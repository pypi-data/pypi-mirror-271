import os
from jinja2 import Environment, FileSystemLoader, Template
import yaml
import gmx.extensions as ex
from gmx.logic.common import CommonLogic

class GenerationLogic:
    def __init__(self) -> None:
        pass

    def apply_extensions(self, env):
        env.globals['lcase'] = ex.lcase
        env.globals['lowercase'] = ex.lowercase
        env.globals['uppercase'] = ex.uppercase
        env.globals['joinify'] = ex.joinify
        env.globals['pluralize'] = ex.pluralize
        env.globals['camel'] = ex.camel
        env.globals['kebab'] = ex.kebab
        env.globals['pascale'] = ex.pascale
        env.globals['dot'] = ex.dot
        env.globals['title'] = ex.title
        env.globals['snake'] = ex.snake
        env.globals['path'] = ex.path
        env.globals['uuid'] = ex.gen_uuid
        env.globals['secret'] = ex.secret
        env.globals['secret_complex'] = ex.secret_complex
        env.globals['get_env'] = ex.get_env
        return env

    def generate_workflow(self, workflow_string, flow_data):
        workflow_template = Template(workflow_string)
        workflow_template.environment = self.apply_extensions(
            workflow_template.environment
        )
        rendered_workflow = workflow_template.render(data=flow_data)
        return rendered_workflow

    def generate(self, item):

        # Load the source data
        data = None
        try:
            data_path = os.path.join(
                item['project_path'], 
                'data', 
                item['data']
            )
            with open(data_path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            print(f'Error: File {data_path} not found.')
        except Exception as e:
            print(f'Error: {e}')


        if data:
            try:
                template_path = os.path.join(
                        item['project_path'], 
                        'templates', 
                        item['template']
                )
                template_content=""
                with open(template_path, 'r') as file:
                    template_content = file.read()
                template = Template(template_content)
                template.environment = self.apply_extensions(
                    template.environment
                )
                output = template.render(data=data)
                CommonLogic.write_content_to_file(output, item['output'])
            except Exception as e:
                print(f'Error rendering template: {e}')
