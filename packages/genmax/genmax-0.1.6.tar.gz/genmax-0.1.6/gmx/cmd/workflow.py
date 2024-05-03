from typing import List, Optional
import typer
from gmx.logic.workflow import WorkFlowLogic
from gmx.logic.preference import PreferenceLogic

workflow_app = typer.Typer(help="Workflow related operations.")

@workflow_app.command(name="run", help="Run a workflow from a specific project.")
def run_workflow(
        workflows: List[str] = typer.Argument(
            ..., 
            help="List the workflows to run."
        ),
        data: Optional[str] = typer.Option(None, "--data", "-d", help="Data for the workflow files.")
    ):
    """
    Run a workflow.

    Args:
        workflows (list): List of workflows to run.
        data (str, optional): Data for the workflow files.
    """
    typer.echo("Running workflow.")
    pl = PreferenceLogic()
    current_proj = pl.get_preference('current_project')
    if current_proj is None:
        typer.echo("Please set a project to run a workflow.")
        return
    wf = WorkFlowLogic()
    wf.run_workflows(current_proj, workflows, data)