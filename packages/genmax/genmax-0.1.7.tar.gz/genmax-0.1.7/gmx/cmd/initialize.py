import typer
from gmx.logic.project import ProjectLogic
from gmx.logic.preference import PreferenceLogic

def init():
    """
    Initialize Genmax.
    """
    typer.echo(f"Initializing Genmax...")
    project_name = "sample"
    pl = ProjectLogic()
    if pl.check_if_exists(project_name):
        typer.echo("Genmax already initialized.")
        typer.echo("Status : Done.")
        return    
    else:
        pl.add_project(project_name)
    typer.echo("Status : Done.")
    pl = PreferenceLogic()
    pl.set_preference('current_project', project_name)
    typer.echo("")
    typer.echo("Run the sample project using the below command:")
    typer.echo(f"gmx wf run {project_name}")
    typer.echo("")
    typer.echo(f"Alternatively, you can pass data to your workflow.")
    typer.echo(f"gmx wf run {project_name} --data=sample")

    