import os
from jinja2 import Environment, FileSystemLoader, Template
import yaml
import gmx.extensions as ex
from gmx.logic.common import CommonLogic

class GenerationLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def apply_extensions(env):
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
        env.globals['env'] = ex.env
        return env

    @staticmethod
    def generate_workflow(workflow_string, flow_data):
        workflow_template = Template(workflow_string)
        workflow_template.environment = GenerationLogic.apply_extensions(
            workflow_template.environment
        )
        rendered_workflow = workflow_template.render(data=flow_data)
        return rendered_workflow

    @staticmethod
    def generate(item):
        env = Environment(loader=FileSystemLoader(
            os.path.join(item['project_path'], 'templates')
            )
        )
        env = GenerationLogic.apply_extensions(env)
        # Load the source data
        try:
            data_path = os.path.join(
                item['project_path'], 
                'data', 
                item['data']
            )
            with open(
                data_path
                ) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)                
        except:
            print(f'Error reading {data_path}.')
        # Load the template
        template = env.get_template(item['template'])
        # Render the template with the source data
        output = template.render(data=data)
        CommonLogic.write_content_to_file(output, item['output'])