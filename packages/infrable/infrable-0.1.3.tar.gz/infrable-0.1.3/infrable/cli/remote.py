from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable

import typer
from tqdm import tqdm

from infrable import Host, files, infra

app = typer.Typer(no_args_is_help=True)


@app.command(name="-")
def from_stdin(command: str):
    """Execute a script on the list of hosts passed via stdin."""

    hosts = []
    for line in typer.get_text_stream("stdin").readlines():
        host = line.split(maxsplit=1)[0].split("@", 1)[-1].strip()
        if not host:
            continue
        for host in infra.filtered_hosts(only=[host]):
            hosts.append(host)

    _execute(hosts, command=command)


@app.command()
def infra_hosts(command: str, only: list[str] = typer.Option(None)):
    """Execute a script on the hosts listed in the infra."""

    hosts = infra.hosts.values()
    if only:
        hosts = infra.filtered_hosts(only=only)

    _execute(hosts, command=command)


@app.command()
def affected_hosts(command: str, only: list[str] = typer.Option(None)):
    """Execute a script on the affected hosts in the last deployment."""

    hosts = files.affected_hosts()

    if only:
        only_hosts = set(h.fqdn for h in infra.filtered_hosts(only=only))
        hosts = (h for h in hosts if h.fqdn in only_hosts)

    _execute(hosts, command=command)


for name, group in infra.host_groups.items():

    def groupmain(command: str, only: list[str] = typer.Option(None)):
        hosts = group
        if only:
            only_hosts = set(h.fqdn for h in infra.filtered_hosts(only=only))
            hosts = (h for h in hosts if h.fqdn in only_hosts)

        _execute(hosts, command=command)

    help = f"Execute a script on {name} hosts."
    app.command(name=name, help=help)(groupmain)


for name, host in infra.hosts.items():

    def hostmaain(command: str):
        host.remote()(command, _fg=True)

    help = f"Execute a script on {name}."
    app.command(name=name, help=help)(hostmaain)


def _execute(hosts: Iterable[Host], command: str):
    hosts = {h.ip: h for h in hosts}.values()
    futures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for h in hosts:
            fut = pool.submit(lambda: (h, h.remote()(command, _err_to_out=True)))
            futures.append(fut)
        print()
        for result in tqdm(as_completed(futures), total=len(futures)):
            host, result = result.result()
            typer.secho(f"╭ {host}", bold=True)
            print(result)
            print()
