# May-02-2024
# utils_directory.py

from pathlib import Path


def init_directory(dir_name):

    dir_path = Path.cwd() / dir_name

    if dir_path.is_dir():
        for child in dir_path.glob('*'):
            if child.is_file():
                child.unlink()
    else:
        create_directory(dir_name)


def create_directory(dir_name):

    dir_path = Path.cwd() / dir_name

    if not dir_path.is_dir():
        dir_path.mkdir()


def remove_directory(dir_name):

    dir_path = Path.cwd() / dir_name

    if dir_path.is_dir():
        for child in dir_path.glob('*'):
            if child.is_file():
                child.unlink()
        dir_path.rmdir()
