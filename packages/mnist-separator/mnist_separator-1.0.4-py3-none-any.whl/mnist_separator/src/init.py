# May-02-2024
# init.py

from mnist_separator.src.clean_all import clean_all
from mnist_separator.src.create_dirs import create_dirs


def init():
    clean_all()
    create_dirs()
