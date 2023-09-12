import os

class Path:
    @staticmethod
    def join(current_file: str, target_path: str) -> str:
        return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(current_file)), target_path))