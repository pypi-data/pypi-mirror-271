import os
import yaml
from gmx.logic.common import CommonLogic
from gmx.logic.generation import GenerationLogic
from gmx.logic.fileops import FileOpsLogic
from gmx.logic.runner import RunnerLogic
from jinja2 import Template


class WorkFlowLogic:
    def __init__(self) -> None:
        pass

    def run_workflows(self, project_name: str, flows: list, flow_data_file: str = None):
        project_path = CommonLogic.get_gmx_folder_path(os.path.join("gmx", project_name))
        for flow in flows:
            self._process_flow(flow, project_path, flow_data_file)

    def _process_flow(self, flow: str, project_path: str, flow_data_file: str = None):
        flow_path = os.path.join(project_path, 'flows', f'{flow}.yaml.j2')
        print(f'Processing Flow: {flow_path}.')
        try:
            if flow_data_file:
                flow_data_path = os.path.join(project_path, 'data', f'{flow_data_file}.yml')
                with open(flow_data_path) as data_file:
                    flow_data = yaml.load(data_file, Loader=yaml.FullLoader)
                with open(flow_path, 'r') as file:
                    workflow_string = file.read()
                rendered_workflow = GenerationLogic.generate_workflow(
                    workflow_string,
                    flow_data
                )
                # workflow_template = Template(workflow_string)
                # rendered_workflow = workflow_template.render(**flow_data)
                items = yaml.safe_load(rendered_workflow)
            else:
                with open(flow_path, 'r') as file:
                    items = yaml.safe_load(file)

            self._process_items(project_path, items)
            print('Flow Status: Done.\n')
        except Exception as e:
            print(f'Flow processing failed: {e}')
            print('Check Flow YAML and filename(s).')

    def _process_items(self, project_path, items):

        # Loop through the items and generate the output files
        for item in items:
            item['project_path'] = project_path
            self._switch_action(
                item["action"],
                item
            )

    def _switch_action(self, argument, param):
        switcher = {
            "generate": GenerationLogic.generate,
            "write_to_file": FileOpsLogic.write_to_file,
            "run_command": RunnerLogic.run_command
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument, self._default_action)
        # Execute the function and return its result
        return func(param)
    
    def _default_action(self, item):
        print("Unrecognized action.")


