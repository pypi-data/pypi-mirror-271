import os
from jinja2 import Environment, FileSystemLoader
from gmx.logic.common import CommonLogic

class FileOpsLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def write_to_file(item):
        env = Environment(loader=FileSystemLoader(
            os.path.join(item['project_path'], 'templates')
            )
        )
        template = env.get_template(item['template'])
        # Render the template with the source data
        output = template.render()
        CommonLogic.write_content_to_file(output, item['output'])

