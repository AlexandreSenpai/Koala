import os

class Path:
    """Utility class for file path operations.

    This class provides a static method for joining paths in a platform-independent manner.

    Methods:
        join: Static method to join the current file path with a target path.
    """

    @staticmethod
    def join(current_file: str, target_path: str) -> str:
        """Joins the current file path with a target path.

        This method takes the current file's path and a target path, and returns an absolute path
        that is the result of joining the two.

        Args:
            current_file: A string representing the path of the current file.
            target_path: A string representing the target path to be joined with the current file path.

        Returns:
            A string representing the absolute path resulting from joining the current file path and target path.
        """
        return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(current_file)), target_path))