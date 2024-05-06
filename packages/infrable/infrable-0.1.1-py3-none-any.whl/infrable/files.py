import random
import shutil
import subprocess as sp
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from difflib import unified_diff
from pathlib import Path
from shlex import quote as q
from typing import IO, Any, Iterable

import typer
from click import Choice
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

from infrable import errors, infra, paths
from infrable.host import Host
from infrable.template import Metadata, render


def affected_hosts(only: Iterable[str] | None = None) -> list[Host]:
    """List the affected hosts as per the files diff."""

    _only = list(infra.filtered_hosts(only=only))
    only_hosts = set(h.ip for h in _only) | set(h.fqdn for h in _only if h.fqdn)

    hosts = {}
    for new in paths.files.glob("**/*.new"):
        old = _old_path(new)
        if not _diff(new=new, old=old):
            continue
        remote, _ = str(new.relative_to(paths.files)).removesuffix(".new").split("/", 1)
        host = remote.split("@", 1)[-1]
        if only and host not in only_hosts:
            continue
        if host not in hosts:
            hosts[host] = infra.get_host(host)
    return list(hosts.values())


def gen(path: Path | None = None, only: Iterable[str] | None = None):
    """Generate files by rendering the templates with context from infra."""

    if paths.files.exists():
        shutil.rmtree(str(paths.files))

    path = path or paths.templates
    templates = Environment(loader=FileSystemLoader(path))

    _only = list(infra.filtered_hosts(only=only))
    only_hosts = set(h.ip for h in _only) | set(h.fqdn for h in _only if h.fqdn)
    for t in templates.list_templates():
        # Render the template metadata
        src = path / t
        typer.secho(f"╭ {src}", bold=True)

        meta = Metadata.parse(src, **infra.items)

        if meta.skip:
            print("╰ skip: true")
            print()
            continue

        for i, dest in enumerate(meta.dest):
            if i + 1 == len(meta.dest):
                print("╰─ ", end="")
            else:
                print("├─ ", end="")

            # Render the template for each destination

            remote, loc = dest.loc.split(":", 1)
            host = remote.split("@", 1)[-1]
            if not host or host == "None" or (only and host not in only_hosts):
                print(f"skipping {dest.loc}")
                continue
            outpath = paths.files / remote / (loc.removeprefix("/") + ".new")
            outpath.parent.mkdir(exist_ok=True, parents=True)
            rendered = render(src, dest_loc=dest.loc, **infra.items, **dest.ctx)
            outpath.write_text(rendered)
            print(outpath)
        print()


def pull():
    """For each generated file pull the current version from the server."""

    if not paths.files.exists():
        return

    for old in paths.files.glob("**/*.old"):
        old.unlink()

    def _pull(new: Path):
        dest = str(new).removesuffix(".new") + ".old"
        remote, loc = (
            str(new.relative_to(paths.files)).removesuffix(".new").split("/", 1)
        )
        src = f"/{loc}"
        name = remote.split("@", 1)[-1]
        host = infra.get_host(name)
        if not host:
            raise errors.InvalidDestinationError(dest=dest)
        addr = f"{host.admin}@{host.ip}"
        _sudo_pull_file(addr, src, dest)
        return new, dest

    futures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for new in paths.files.glob("**/*.new"):
            futures.append(pool.submit(_pull, new))
        print()
        for result in tqdm(as_completed(futures, timeout=2 * 60), total=len(futures)):
            new, dest = result.result()
            typer.secho(f"╭ {new}", bold=True)
            print(f"╰ {dest}")
            print()


def backup():
    """Backup the files locally."""

    if not paths.files.exists():
        return

    dirname = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    backupdir = paths.backups / dirname
    shutil.copytree(str(paths.files), str(backupdir))
    print()
    print(f"backup: {backupdir}")
    print()


def diff():
    """Diff the generated files with the pulled versions."""

    for new in paths.files.glob("**/*.new"):
        old = _old_path(new)
        if d := _diff(new=new, old=old):
            _print_diff(d)
            print()
            print()
            print()


def push(yes: bool = False):
    """Diff and push the generated files to the remote server."""

    for new in paths.files.glob("**/*.new"):
        remote, loc = (
            str(new.relative_to(paths.files)).removesuffix(".new").split("/", 1)
        )

        old = _old_path(new)
        remote_dest = f"{remote}:/{loc}"

        if d := _diff(new=new, old=old):
            _print_diff(d)
            if not yes:
                ans = typer.prompt(
                    f"Push?", type=Choice(["y", "n", "all"]), default="y"
                )
                match ans.lower():
                    case "n":
                        new.unlink()
                        old.unlink()
                        continue
                    case "all":
                        yes = True

            meta = Metadata.parse(new)
            dest = next(d for d in meta.dest if d.loc == remote_dest)
            chown = dest.chown or meta.chown
            chmod = dest.chmod or meta.chmod
            dest = f"/{loc}"
            name = remote.split("@", 1)[-1]
            host = infra.get_host(name)
            if not host:
                raise errors.InvalidDestinationError(dest)
            addr = f"{host.admin}@{host.ip}"
            _sudo_push_file(addr, new, dest, chown=chown, chmod=chmod)
        else:
            print(f"skipping {remote_dest}")
            new.unlink()
            old.unlink()
        print()
        print()
        print()


def revert(path: Path | None = None):
    """Revert files from backup."""

    if path is None:
        path = max(paths.backups.glob("*"))

    print(f"reverting from: {path}")

    for bkold in path.glob("**/*.old"):
        bknew = Path(str(bkold).removesuffix(".old") + ".new")

        old = paths.files / bkold.relative_to(path)
        new = paths.files / bknew.relative_to(path)

        typer.secho(f"╭ {new}", bold=True)
        shutil.copy(str(bkold), str(new))

        print(f"╰ {old}")
        shutil.copy(str(bknew), str(old))


def deploy(
    path: Path | None = None, only: Iterable[str] | None = None, yes: bool = False
):
    """[WORKFLOW] generate, pull, backup, compare and push the generated files to the remote server."""

    if path or yes or typer.confirm("Generate fresh files?", default=True, err=True):
        gen(path, only=only)
        pull()
        backup()
    elif typer.confirm("Pull files from remote?", default=True, err=True):
        pull()
        backup()
    elif typer.confirm("Backup files locally?", default=True, err=True):
        backup()

    push(yes=yes)


def recover(path: Path | None = None):
    """[WORKFLOW] revert and push files from backup."""

    revert(path)
    push()


def _old_path(new: Path) -> Path:
    return Path(str(new).removesuffix(".new") + ".old")


def _diff(new: Path, old: Path) -> list[str]:
    new_lines = new.read_text().splitlines()
    old_lines = Path(old).read_text().splitlines()
    return list(unified_diff(old_lines, new_lines, fromfile=str(old), tofile=str(new)))


def _print_diff(diff: list[str]):
    for line in diff:
        if line.startswith("---"):
            typer.secho(line, fg=typer.colors.RED, bold=True)
        elif line.startswith("+++"):
            typer.secho(line, fg=typer.colors.GREEN, bold=True)
        elif line.startswith("-"):
            typer.secho(line, fg=typer.colors.RED)
        elif line.startswith("+"):
            typer.secho(line, fg=typer.colors.GREEN)

        elif line.startswith("@"):
            typer.secho(line, dim=True)
        else:
            print(line)


def _sudo_exec(
    address: str,
    command: list[str] | str,
    options: list[str] | None = None,
    shell: str | None = None,
    stdout: int | IO[Any] = sp.PIPE,
    stderr: int | IO[Any] = sp.PIPE,
    stdin: int | IO[Any] = sp.PIPE,
) -> sp.CompletedProcess[bytes]:
    if isinstance(command, list):
        command = sp.list2cmdline(command)
    if shell:
        command = sp.list2cmdline([shell, "-c", q(command)])
    options = options or []
    return sp.run(
        [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            *options,
            address,
            command,
        ],
        stdout=stdout,
        stderr=stderr,
        stdin=stdin,
    )


def _sudo_pull_file(address: str, remote_src: str, local_dest: str):
    with Path(local_dest).open("w") as f:
        _sudo_exec(
            address,
            f"sudo cat -- {q(remote_src)} || true",
            stdout=f,
            stderr=sp.PIPE,
            stdin=sp.PIPE,
        ).check_returncode()


def _sudo_push_file(
    address: str,
    local_src,
    remote_dest,
    chmod: str | None = None,
    chown: str | None = None,
):
    ts = time.time()
    rand = random.randint(0, 9999)
    tmpname = f"/tmp/infrable-push-{ts}.{rand}"
    parent = str(Path(remote_dest).parent)
    cmd = f"sudo tee -- {q(tmpname)}"  # as root for security

    # Change permissions and ownership before moving to final destination.
    # Else, you might end up getting locked from the server.
    if chmod:
        cmd = f"{cmd} && sudo chmod -- {q(chmod)} {q(tmpname)}"

    if chown:
        cmd = f"{cmd} && sudo chown -- {q(chown)} {q(tmpname)}"

    cmd += f" && sudo mkdir -p -- {q(parent)}"
    cmd += f" && sudo mv -f -- {q(tmpname)} {q(remote_dest)}"

    with Path(local_src).open("r") as f:
        _sudo_exec(address, cmd, stdin=f).check_returncode()
