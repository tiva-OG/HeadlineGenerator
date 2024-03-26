import os
import yaml
from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations
from box.exceptions import BoxValueError
from headlineGenerator.logging import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    reads yaml file and return its contents
    raises ValueError if yaml file is empty

    :param path_to_yaml: path-like input of type `Path`
    :return content: `ConfigBox` type object
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file : {path_to_yaml} loaded successfully")

            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    creates `list` of directories

    :param path_to_directories: a list containing path to directories
    :param verbose: `bool` to display info on the process or not
    :return:
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """
    get size of file in KB

    :param path: path to file
    :return size_in_kb: `str` indicating file size
    """
    size_in_kb = round(os.path.getsize(path) / 1024)

    return f"~ {size_in_kb}KB"
