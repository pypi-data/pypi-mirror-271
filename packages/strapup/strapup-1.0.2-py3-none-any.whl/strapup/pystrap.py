
import os
from sys import path as syspath
from .logger import Logger

# root = 'module_name'
# log_name = 'scrappy'
# log_level = 'debug'
# log_level = 'info'
# log_level = 'error'
# log_level = 'warning'

# log_to_file = True
# log_to_file = False




class Strapup:
    def __init__(self, package_name: str = None, log_file_name: str = None, log_to_file: bool = True, log_level: str = 'info'):
        if package_name is not None:
            self.package_name = package_name
            self.package_path = self._find_directory(self.package_name)
            self._add_to_pythonpath(os.path.normpath(f'{self.package_path}/../'))

        self.LOG = None
        self.LOG = self.get_logger(log_file_name=log_file_name, log_to_file=log_to_file, log_level=log_level)
        # LOG.disable_file_output()
        # LOG.disable_console_output()

    def get_logger(self, log_file_name: str = None, log_to_file: bool = True, log_level: str = 'info') -> Logger:
        if log_file_name is not None:
            self.LOG = Logger(name=log_file_name, log_to_file=log_to_file, log_level=log_level)
        return self.LOG

    def _find_directory(self, dir_name, max_upper_levels_to_check=2, root_dir=None) -> str:
        if root_dir is None:
            root_dir = os.getcwd()
        path = None
        if max_upper_levels_to_check <= -1:
            return None
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if dir_name in dirnames:
                return os.path.join(dirpath, dir_name)
        if path is None:
            return os.path.normpath(self._find_directory(dir_name, max_upper_levels_to_check - 1, f'{root_dir}/../'))

    def _add_to_pythonpath(self, module_path) -> str:
        if module_path is None:
            return 1, ''
        if module_path not in syspath:
            syspath.insert(0, module_path)
        return module_path


