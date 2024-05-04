import os
import subprocess
import platform

class CommonLogic:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_gmx_folder_path(folder_path):
        if platform.system() != "Windows":
            folder_path = "_" + folder_path
        return folder_path
    
    @staticmethod
    def write_content_to_file(content, filepath):
        try:
            # Check if the folder path exists, if not, create it
            current_working_directory = os.getcwd()
            raw_path = filepath.replace(">",os.sep)
            folder_path = os.path.dirname(raw_path)
            folder_path = os.path.join(
                current_working_directory,
                folder_path
            )
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # Check if the file exists, if not, create it
            with open(raw_path, 'w') as file:
                    file.write(content)
        except Exception as e:
            print(e)
            filepath = filepath
            print(f'Error writing output {filepath}')
