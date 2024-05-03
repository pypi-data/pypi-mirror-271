# May-02-2024
# magnitude.py

import cv2 as cv
import numpy as np

from mnist_separator.src import cfg


def get_magn_roi(any_image: np.uint8) -> np.ndarray:

    height = any_image.shape[0]
    width = any_image.shape[1]

    array_dft = \
        np.zeros((cfg.size_dft, cfg.size_dft), dtype=np.float32)

    array_dft[0:height:, 0:width:] = any_image[0::, 0::]

    dft = cv.dft(array_dft, flags=cv.DFT_COMPLEX_OUTPUT)

    dft_shift = np.fft.fftshift(dft)

    re_shift = dft_shift[:, :, 0]
    im_shift = dft_shift[:, :, 1]

    re_roi = np.zeros((cfg.size_roi, cfg.size_roi), dtype=np.float32)
    im_roi = np.zeros((cfg.size_roi, cfg.size_roi), dtype=np.float32)
    magn_roi_norm = np.zeros((cfg.size_roi, cfg.size_roi), dtype=np.float32)

    y0 = (cfg.size_dft - cfg.size_roi) // 2
    x0 = y0

    re_roi[0:cfg.size_roi:, 0:cfg.size_roi:] = \
        re_shift[y0:y0+cfg.size_roi:, x0:x0+cfg.size_roi:]
    im_roi[0:cfg.size_roi:, 0:cfg.size_roi:] = \
        im_shift[y0:y0+cfg.size_roi:, x0:x0+cfg.size_roi:]

    magn_roi = cv.magnitude(re_roi, im_roi)

    cv.normalize(magn_roi, magn_roi_norm, 0, 255, cv.NORM_MINMAX)

    return magn_roi_norm


def get_magn_half(magn_roi: np.ndarray) -> np.ndarray:

    size_roi_half_1 = cfg.size_roi_half + 1

    shape_magn_half = (size_roi_half_1, cfg.size_roi)

    magn_half = np.empty(shape_magn_half, dtype=np.float32)

    magn_half[0:size_roi_half_1, 0:cfg.size_roi] = \
        magn_roi[0:size_roi_half_1:, 0::]

    return magn_half
