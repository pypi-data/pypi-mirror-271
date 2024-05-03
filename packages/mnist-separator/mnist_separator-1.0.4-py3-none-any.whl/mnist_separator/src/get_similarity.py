# May-02-2024
# get_similarity.py

import sys
import cv2 as cv

from mnist_separator.src.to_canonical import to_canonical
from mnist_separator.src.calc_similarity import calc_similarity


def get_similarity(path_1: str, path_2: str) -> float:

    image1_mnist = cv.imread(path_1, cv.IMREAD_UNCHANGED)
    if image1_mnist is None:
        print(f'\nERROR: Unable to read {path_1}.')
        sys.exit(1)

    image2_mnist = cv.imread(path_2, cv.IMREAD_UNCHANGED)
    if image2_mnist is None:
        print(f'\nERROR: Unable to read {path_2}.')
        sys.exit(1)

    image1_canon = to_canonical(image1_mnist)
    image2_canon = to_canonical(image2_mnist)

    similarity = calc_similarity(image1_canon, image2_canon)

    return similarity
