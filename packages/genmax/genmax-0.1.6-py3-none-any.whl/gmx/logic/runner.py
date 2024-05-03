import os

class RunnerLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def run_command(item):
        try:
            os.system(item['command'])
        except Exception as e:
            print(f"An error occurred: {e}")