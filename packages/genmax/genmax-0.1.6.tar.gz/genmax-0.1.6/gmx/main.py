import typer
from gmx.cmd.workflow import workflow_app
from gmx.cmd.project import project_app
from gmx.cmd.initialize import init

app = typer.Typer()
app.add_typer(workflow_app, name="wf")
app.add_typer(project_app, name="proj")
app.command()(init)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Generate code using gmx.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Welcome to Genmax!!")
        typer.echo("To explore commands at any time, type:")
        typer.echo("gmx --help")

if __name__ == "__main__":
    app()