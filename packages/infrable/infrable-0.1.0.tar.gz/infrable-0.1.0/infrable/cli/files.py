from pathlib import Path

import typer

from infrable import files

app = typer.Typer(no_args_is_help=True)


@app.command(help=files.affected_hosts.__doc__)
def affected_hosts(only: list[str] = typer.Option(None)):
    for host in files.affected_hosts(only=only):
        print(host)


@app.command(help=files.deploy.__doc__)
def deploy(
    path: Path = typer.Argument(None),
    only: list[str] = typer.Option(None),
    yes: bool = False,
):
    files.deploy(path, only=only, yes=yes)


@app.command(help=files.recover.__doc__)
def recover(path: Path = typer.Argument(None)):
    files.recover(path)


@app.command(help=files.gen.__doc__)
def gen(
    path: Path = typer.Argument(None),
    only: list[str] = typer.Option(None),
):
    files.gen(path, only=only)


app.command()(files.backup)
app.command()(files.pull)
app.command()(files.diff)
app.command()(files.push)


@app.command(help=files.revert.__doc__)
def revert(path: Path = typer.Argument(None)):
    files.revert(path)
