# May-02-2024
# utils_list.py

import os
from pathlib import Path


def save_list(list_name, dir_name, any_list):

    fname = Path.cwd() / dir_name / list_name

    with open(fname, 'w') as fname:
        for item in any_list:
            fname.write(f'{item}\n')


def print_list(tag, any_list):
    print(f'{tag}:')
    n = 0
    for item in any_list:
        print(f'{n}:\t {item}')
        n += 1


def list_visible_files(dir_name):
    visible_files = []
    for file in os.listdir(dir_name):
        if not file.startswith('.'):
            visible_files.append(file)
    return visible_files
