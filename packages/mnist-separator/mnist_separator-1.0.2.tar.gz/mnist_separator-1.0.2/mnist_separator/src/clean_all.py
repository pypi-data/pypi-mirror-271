# May-02-2024
# clean_all.py

from pathlib import Path

from mnist_separator.src import glbl
from mnist_separator.src.utils_directory import init_directory


def clean_all():

    init_directory(glbl.result_name)

    path_mnist = Path.cwd() / '$mnist'
    path_conon = Path.cwd() / '$canon'

    if path_mnist.is_dir():
        rmtree(path_mnist)
    if path_conon.is_dir():
        rmtree(path_conon)


def rmtree(root):

    for p in root.iterdir():
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()

    root.rmdir()
