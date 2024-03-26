import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] : %(message)s")

project_name = "headlineGenerator"

list_of_files = [
    ".github/workflows/.gitkeep",
    ".gitignore",
    "Dockerfile",
    "research/trials.ipynb",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/logging/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    "config.yaml",
    "params.yaml",
    "app.py",
    "main.py",
    "setup.py",
    "requirements.txt"
]

for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir, file_name = os.path.split(file_path)

    # create parent directory for files with parent directories
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating directory : {file_dir} for file : {file_name}")

    # check if file doesn't exist or is empty before creating new one
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        logging.info(f"Creating new file : {file_path}")
        with open(file_path, "w") as _:
            pass
    else:
        logging.info(f"{file_path} already exists")