import os
from jinja2 import Environment, FileSystemLoader
from gmx.logic.common import CommonLogic

class FileOpsLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def write_to_file(item):
        template_path = os.path.join(
                item['project_path'], 
                'templates', 
                item['template']
        )
        with open(template_path, 'r') as file:
            template_content = file.read()
        output = template_content
        CommonLogic.write_content_to_file(output, item['output'])

