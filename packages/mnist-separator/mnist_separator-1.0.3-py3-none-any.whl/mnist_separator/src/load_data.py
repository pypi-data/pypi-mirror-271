# May-02-2024
# load_data.py

import sys
import os
import shutil
from pathlib import Path


def load_data(dir_mnist, digit, num_images):

    if dir_mnist.exists() and dir_mnist.is_dir():

        dir_src = dir_mnist / 'data_test' / str(digit)

        dir_dst = Path.cwd() / '$mnist' / 'test'

        # Get a list of files in the source directory
        files = os.listdir(dir_src)

        # Sort the files based on their creation time or modification time
        files.sort(key=lambda x: os.path.getmtime(os.path.join(dir_src, x)))

        # Copy each file from the source directory to the destination directory
        n = 0
        for file in files:
            src_file_path = os.path.join(dir_src, file)
            dst_file_path = os.path.join(dir_dst, file)
            shutil.copy(src_file_path, dst_file_path)
            n += 1
            if n == num_images:
                break
    else:
        sys.exit(f"\nDirectory {dir_mnist} does not exist.")
