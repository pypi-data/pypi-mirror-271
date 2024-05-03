# May-02-2024
# convert_data.py

import cv2 as cv
import os
from pathlib import Path

from mnist_separator.src import glbl
from mnist_separator.src.to_canonical import to_canonical


glbl.path_test_mnist = str(Path.cwd() / '$mnist' / 'test')
glbl.path_train_0_mnist = str(Path.cwd() / '$mnist' / 'train_0')
glbl.path_train_1_mnist = str(Path.cwd() / '$mnist' / 'train_1')
glbl.path_train_2_mnist = str(Path.cwd() / '$mnist' / 'train_2')
glbl.path_train_3_mnist = str(Path.cwd() / '$mnist' / 'train_3')
glbl.path_train_4_mnist = str(Path.cwd() / '$mnist' / 'train_4')
glbl.path_train_5_mnist = str(Path.cwd() / '$mnist' / 'train_5')
glbl.path_train_6_mnist = str(Path.cwd() / '$mnist' / 'train_6')
glbl.path_train_7_mnist = str(Path.cwd() / '$mnist' / 'train_7')
glbl.path_train_8_mnist = str(Path.cwd() / '$mnist' / 'train_8')
glbl.path_train_9_mnist = str(Path.cwd() / '$mnist' / 'train_9')

glbl.path_test_canon = str(Path.cwd() / '$canon' / 'test')
glbl.path_train_0_canon = str(Path.cwd() / '$canon' / 'train_0')
glbl.path_train_1_canon = str(Path.cwd() / '$canon' / 'train_1')
glbl.path_train_2_canon = str(Path.cwd() / '$canon' / 'train_2')
glbl.path_train_3_canon = str(Path.cwd() / '$canon' / 'train_3')
glbl.path_train_4_canon = str(Path.cwd() / '$canon' / 'train_4')
glbl.path_train_5_canon = str(Path.cwd() / '$canon' / 'train_5')
glbl.path_train_6_canon = str(Path.cwd() / '$canon' / 'train_6')
glbl.path_train_7_canon = str(Path.cwd() / '$canon' / 'train_7')
glbl.path_train_8_canon = str(Path.cwd() / '$canon' / 'train_8')
glbl.path_train_9_canon = str(Path.cwd() / '$canon' / 'train_9')


def convert_data():
    mnist_to_canonical(glbl.path_test_mnist, glbl.path_test_canon)

    mnist_to_canonical(glbl.path_train_0_mnist, glbl.path_train_0_canon)
    mnist_to_canonical(glbl.path_train_1_mnist, glbl.path_train_1_canon)
    mnist_to_canonical(glbl.path_train_2_mnist, glbl.path_train_2_canon)
    mnist_to_canonical(glbl.path_train_3_mnist, glbl.path_train_3_canon)
    mnist_to_canonical(glbl.path_train_4_mnist, glbl.path_train_4_canon)
    mnist_to_canonical(glbl.path_train_5_mnist, glbl.path_train_5_canon)
    mnist_to_canonical(glbl.path_train_6_mnist, glbl.path_train_6_canon)
    mnist_to_canonical(glbl.path_train_7_mnist, glbl.path_train_7_canon)
    mnist_to_canonical(glbl.path_train_8_mnist, glbl.path_train_8_canon)
    mnist_to_canonical(glbl.path_train_9_mnist, glbl.path_train_9_canon)


def mnist_to_canonical(dir_name_in, dir_name_out):

    for fname in os.listdir(dir_name_in):

        if fname.startswith('.'):
            continue

        path_in = dir_name_in + '/' + fname
        path_out = dir_name_out + '/' + fname

        image_mnist = cv.imread(path_in, cv.IMREAD_GRAYSCALE)

        image_canon = to_canonical(image_mnist)

        cv.imwrite(path_out, image_canon)
