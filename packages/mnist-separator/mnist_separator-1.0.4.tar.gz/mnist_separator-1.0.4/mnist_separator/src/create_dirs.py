# May-02-2024
# create_dirs.py

from pathlib import Path
import os


def create_dirs():
    create_mnist_dirs()
    create_canon_dirs()


def create_mnist_dirs():

    dir_name = '$mnist'
    dir_path = Path.cwd() / dir_name

    result = os.path.isdir(dir_path)
    if result:
        return
    else:
        dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'test'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_0'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_1'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_2'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_3'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_4'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_5'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_6'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_7'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_8'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_9'
    dir_path.mkdir()


def create_canon_dirs():

    dir_name = '$canon'
    dir_path = Path.cwd() / dir_name

    result = os.path.isdir(dir_path)
    if result:
        return
    else:
        dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'test'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_0'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_1'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_2'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_3'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_4'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_5'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_6'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_7'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_8'
    dir_path.mkdir()

    dir_path = Path.cwd() / dir_name / 'train_9'
    dir_path.mkdir()
