# May-02-2024
# to_canonical.py

import cv2 as cv
import numpy as np


def to_canonical(image_in):

    width = 128
    height = 128

    # dim = (width, height)
    image_resize = cv.resize(image_in, (width, height), cv.INTER_LANCZOS4)

    threshold, image_thr \
        = cv.threshold(image_resize, 0, 255,
                       cv.THRESH_BINARY + cv.THRESH_OTSU)

    image_correlation = get_correlation(image_thr)

    threshold, image_out \
        = cv.threshold(image_correlation, 0, 255,
                       cv.THRESH_BINARY + cv.THRESH_OTSU)

    return image_out


def get_correlation(scene):

    # Calc DFT dimension.
    # ---------------------------------------------------------
    scene_rows = scene.shape[0]
    scene_cols = scene.shape[1]

    height_dft = 256
    width_dft = 256
    dft_shape = (height_dft, width_dft)
    # ---------------------------------------------------------

    # Scene
    # ---------------------------------------------------------
    scene_array_dft = np.zeros(dft_shape, dtype=np.float32)

    scene_array_dft[0:scene_rows, 0:scene_cols] = scene[0::, 0::]

    scene_dft = cv.dft(scene_array_dft, flags=cv.DFT_COMPLEX_OUTPUT)
    # ---------------------------------------------------------

    # Pattern
    # ---------------------------------------------------------
    pattern_size: int = 1
    pattern_rows = pattern_size
    pattern_cols = pattern_size
    pattern_shape = (pattern_rows, pattern_cols)
    pattern = np.empty(pattern_shape, dtype=np.uint8)
    pattern.fill(255)
    # ---------------------------------------------------------
    pattern_array_dft = np.zeros(dft_shape, dtype=np.float32)

    pattern_array_dft[
                height_dft - pattern_rows:height_dft:,
                width_dft - pattern_cols:width_dft:] = pattern[0::, 0::]

    pattern_dft = cv.dft(pattern_array_dft, flags=cv.DFT_COMPLEX_OUTPUT)
    # ---------------------------------------------------------

    # Product 1
    # ---------------------------------------------------------
    product1_dft = np.zeros((height_dft, width_dft, 2), dtype=np.float32)

    dft_mul(scene_dft, pattern_dft, product1_dft)
    # ---------------------------------------------------------

    #  Laplace filtering
    # ---------------------------------------------------------
    array_dft = laplace(height_dft, width_dft)

    filter_dft = cv.dft(array_dft, flags=cv.DFT_COMPLEX_OUTPUT)
    # ---------------------------------------------------------

    # Product 2
    # ---------------------------------------------------------
    product2_dft = np.zeros((height_dft, width_dft, 2), dtype=np.float32)

    dft_mul(product1_dft, filter_dft, product2_dft)
    # ---------------------------------------------------------

    # Inverse product2_dft.
    # ---------------------------------------------------------
    inverse_product2_dft = cv.idft(product2_dft)

    re = inverse_product2_dft[:, :, 0]

    re[re < 0.0] = 0.0
    # ---------------------------------------------------------

    # Get Correlation.
    # ---------------------------------------------------------
    correlation = np.zeros((scene_rows, scene_cols), dtype='float32')
    correlation_norm = np.zeros((scene_rows, scene_cols), dtype=np.float32)

    correlation[0::, 0::] = re[0:scene_rows:, 0:scene_cols:]

    cv.normalize(correlation, correlation_norm, 0, 255, cv.NORM_MINMAX)
    # ---------------------------------------------------------

    return np.uint8(correlation_norm)


def dft_mul(src1, src2, dst):

    x1 = src1[:, :, 0]
    y1 = src1[:, :, 1]

    x2 = src2[:, :, 0]
    y2 = src2[:, :, 1]

    dst[:, :, 0] = (x1 * x2) - (y1 * y2)
    dst[:, :, 1] = (x1 * y2) + (x2 * y1)


def laplace(height_dft, width_dft):

    array_filter = np.zeros((height_dft, width_dft), dtype='float32')

    array_filter[0, 0] = -1
    array_filter[0, 1] = -1
    array_filter[0, 2] = -1

    array_filter[1, 0] = -1
    array_filter[1, 1] = 8
    array_filter[1, 2] = -1

    array_filter[2, 0] = -1
    array_filter[2, 1] = -1
    array_filter[2, 2] = -1

    return array_filter
