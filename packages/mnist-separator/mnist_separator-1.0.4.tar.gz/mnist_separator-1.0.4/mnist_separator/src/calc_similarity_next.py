# May-02-2024
# calc_similarity_next.py

import numpy as np

from mnist_separator.src import cfg


def calc_similarity_next(
        magnitude_1: np.float32,
        magnitude_2: np.float32) -> float:

    arr_zero = np.zeros(cfg.dsize_roi, dtype=np.float32)
    arr_1 = np.maximum(magnitude_1, arr_zero)
    arr_2 = np.maximum(magnitude_2, arr_zero)

    arr_min = np.minimum(arr_1, arr_2)
    arr_max = np.maximum(arr_1, arr_2)

    similarity_map = np.subtract(arr_max, arr_min, where=arr_min > 0)
    nonzero_count = np.count_nonzero(similarity_map)

    if nonzero_count == 0:
        similarity = 1.0
    else:
        average = np.sum(similarity_map) / nonzero_count
        similarity = 1.0 / (1.0 + cfg.param_similarity * average)

    return similarity
