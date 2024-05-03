# May-02-2024
# get_similarity_group.py

import os
import cv2 as cv
import numpy as np

from mnist_separator.src.calc_similarity import calc_similarity


def get_similarity_group(path_image_test: str, path_train: str) -> float:
    """
    Нахождение максимального значения степени сходства между
    заданным каноническим изображением и всеми каноническими
    изображениями группы.
    """

    similarity_group: float = 0

    list_train = list_visible_files(path_train)
    if len(list_train) == 0:
        return similarity_group

    image_canon = cv.imread(path_image_test, cv.IMREAD_UNCHANGED)

    for fname in list_train:

        path_image_train = path_train + '/' + fname
        image_train_canon = cv.imread(path_image_train, cv.IMREAD_UNCHANGED)

        similarity = calc_similarity(np.uint8(image_canon), np.uint8(image_train_canon))

        similarity_group = max(similarity, similarity_group)

    return similarity_group


def list_visible_files(dir_name):
    visible_files = []
    for file in os.listdir(dir_name):
        if not file.startswith('.'):
            visible_files.append(file)
    return visible_files
