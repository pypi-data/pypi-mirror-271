from .pystrap import Strapup
from .logger import Logger


def init(package_name: str) -> None:
    Strapup(package_name=package_name)


def strap_up(package_name: str) -> None:
    init(package_name=package_name)


def get_logger(log_file_name:str, log_to_file: bool = True, log_level: str = 'info') -> Logger:
    strap = Strapup(log_file_name=log_file_name, log_to_file=log_to_file, log_level=log_level)
    return strap.get_logger()
