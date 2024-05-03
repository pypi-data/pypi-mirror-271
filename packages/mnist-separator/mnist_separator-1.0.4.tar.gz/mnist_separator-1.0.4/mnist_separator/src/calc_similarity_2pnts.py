# May-02-2024
# calc_similarity_2pnts.py

import cv2 as cv
import numpy as np
import math

from mnist_separator.src import cfg
from mnist_separator.src.calc_similarity_next import calc_similarity_next
from mnist_separator.src.get_angle import get_angle_axe_x


def calc_similarity_2pnts(
                image_magn_roi, templ_magn_roi,
                image_list_of_peaks_calc,
                templ_list_of_peaks_calc) -> float:

    image_table_2pnts = create_table_2pnts(image_list_of_peaks_calc)
    n_image_peaks = len(image_list_of_peaks_calc)

    templ_table_2pnts = create_table_2pnts(templ_list_of_peaks_calc)
    n_templ_peaks = len(templ_list_of_peaks_calc)

    similarity_result: float = 0
    for j in range(n_image_peaks):

        length_src = image_table_2pnts[j, 2]
        angle_src = image_table_2pnts[j, 3]

        for i in range(n_templ_peaks):

            length_dst = templ_table_2pnts[i, 2]
            angle_dst = templ_table_2pnts[i, 3]

            angle: float = float(angle_dst - angle_src)
            scale: float = float(length_dst / length_src)
            mat_rotate = cv.getRotationMatrix2D(cfg.center, angle, scale)

            image_magn_roi_warp \
                = cv.warpAffine(image_magn_roi, mat_rotate, cfg.dsize_roi)

            similarity_current \
                = calc_similarity_next(np.float32(image_magn_roi_warp),
                                       np.float32(templ_magn_roi))

            if similarity_current > similarity_result:
                similarity_result = similarity_current

    return similarity_result


def create_table_2pnts(list_of_peaks) -> np.ndarray:

    table_rows = len(list_of_peaks)
    table_cols = 4

    table = np.zeros((table_rows, table_cols), dtype=np.float32)

    for n in range(table_rows):

        peak = list_of_peaks[n]
        y_peak = peak[0]
        x_peak = peak[1]

        # coordinates
        table[n, 0] = x_peak
        table[n, 1] = y_peak

        # length
        dx: float = x_peak - cfg.X0
        dy: float = y_peak - cfg.Y0
        table[n, 2] = math.sqrt((dx * dx) + (dy * dy))

        # angle
        table[n, 3] = get_angle_axe_x(x_peak, y_peak)

    return table
