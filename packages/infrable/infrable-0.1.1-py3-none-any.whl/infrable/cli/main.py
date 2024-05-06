import sys

import typer

from infrable import __version__, errors, infra, init
from infrable.cli import files, remote, switch

app = typer.Typer(no_args_is_help=True)


@app.command()
def version():
    """Print the version."""
    print(f"infrable {__version__}")


@app.command()
def hosts(format: str | None = None, repr: bool = False):
    """List all hosts in the infrastructure."""

    for name, host in infra.hosts.items():
        if format:
            print(host.format(name, format=format))
        elif repr:
            print(f"{name} = {host.__repr__()}")
        else:
            print(f"{name} = {host}")


@app.command()
def services(format: str | None = None, repr: bool = False):
    """List all services in the infrastructure."""

    for name, service in infra.services.items():
        if format:
            print(service.format(name, format=format))
        elif repr:
            print(f"{name} = {service.__repr__()}")
        else:
            print(f"{name} = {service}")


@app.command()
def switches(format: str | None = None, repr: bool = False):
    """List all switches in the infrastructure."""

    for name, switch in infra.switches.items():
        if format:
            print(switch.format(name, format=format))
        elif repr:
            print(f"{name} = {switch.__repr__()}")
        else:
            print(f"{name} = {switch}")


@app.command(name="init")
def init_():
    """Bootstrap a dummy project."""
    init.init()


app.add_typer(files.app, name="files", help="Manage files.")
app.add_typer(switch.app, name="switch", help="Manage switches.")
app.add_typer(remote.app, name="remote", help="Execute remote commands.")

for name, ext in infra.typers.items():
    app.add_typer(ext, name=name.replace("_", "-"))


if __name__ == "__main__":
    try:
        app()
    except errors.Error as e:
        print(e, file=sys.stderr)
        raise typer.Exit(1) from e
