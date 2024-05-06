import typer
from click import Choice

from infrable import infra

app = typer.Typer(no_args_is_help=True)


for name, sw in infra.switches.items():
    help = f"Set the value of the {name} switch."

    def main(value: str = typer.Argument(..., click_type=Choice(list(sw.options)))):
        sw.set(value)

    app.command(name=name, help=help)(main)
