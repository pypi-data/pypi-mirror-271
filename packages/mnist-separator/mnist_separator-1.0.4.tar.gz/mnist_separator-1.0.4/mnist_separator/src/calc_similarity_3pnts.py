# May-02-2024
# calc_similarity_3pnts.py

import cv2 as cv
import numpy as np

from mnist_separator.src import cfg
from mnist_separator.src.calc_similarity_next import calc_similarity_next
from mnist_separator.src.get_angle import get_angle_axe_x


def calc_similarity_3pnts(
                image_magn_roi, templ_magn_roi,
                image_list_of_peaks_calc,
                templ_list_of_peaks_calc) -> float:

    image_table, n_image_table_rows = create_table_3pnts(image_list_of_peaks_calc)
    templ_table, n_templ_table_rows = create_table_3pnts(templ_list_of_peaks_calc)

    similarity_result: float = 0
    for j in range(n_image_table_rows):

        angle_image: int = image_table[j, 4]

        if angle_image > 0:
            y1_image = image_table[j, 0]
            x1_image = image_table[j, 1]
            y2_image = image_table[j, 2]
            x2_image = image_table[j, 3]
        else:
            y1_image = image_table[j, 2]
            x1_image = image_table[j, 3]
            y2_image = image_table[j, 0]
            x2_image = image_table[j, 1]

        for i in range(n_templ_table_rows):

            angle_templ: int = templ_table[i, 4]

            if angle_templ > 0:
                y1_templ = templ_table[i, 0]
                x1_templ = templ_table[i, 1]
                y2_templ = templ_table[i, 2]
                x2_templ = templ_table[i, 3]
            else:
                y1_templ = templ_table[i, 2]
                x1_templ = templ_table[i, 3]
                y2_templ = templ_table[i, 0]
                x2_templ = templ_table[i, 1]

            # angle filter
            angle_image = abs(angle_image)
            angle_templ = abs(angle_templ)
            if angle_image > angle_templ:
                angle_ratio: float = float(angle_image) / float(angle_templ)
            else:
                angle_ratio: float = float(angle_templ) / float(angle_image)

            if angle_ratio > cfg.angle_ratio_threshold:
                continue

            pts_image = np.float32([[x1_image, y1_image],
                                    [x2_image, y2_image],
                                    [cfg.X0, cfg.Y0]])

            pts_templ = np.float32([[x1_templ, y1_templ],
                                    [x2_templ, y2_templ],
                                    [cfg.X0, cfg.Y0]])

            mat_affine = cv.getAffineTransform(pts_image, pts_templ)

            image_magn_roi_warp \
                = cv.warpAffine(image_magn_roi, mat_affine, cfg.dsize_roi)

            similarity_current \
                = calc_similarity_next(np.float32(image_magn_roi_warp),
                                       np.float32(templ_magn_roi))

            if similarity_current > similarity_result:
                similarity_result = similarity_current

    return similarity_result


def create_table_3pnts(list_of_peaks) -> (np.ndarray, int):

    n_peaks: int = len(list_of_peaks)

    first_table = np.zeros((n_peaks, 2), dtype=np.int32)

    for n in range(n_peaks):
        peak = list_of_peaks[n]
        first_table[n, 0] = peak[0]  # y пикa
        first_table[n, 1] = peak[1]  # x пикa

    n_second_table: int = (n_peaks * n_peaks - n_peaks) // 2

    second_table = np.zeros((n_second_table, 5), dtype=np.int32)

    n_rows: int = 0
    for j in range(n_peaks - 1):

        y1 = int(first_table[j, 0])
        x1 = int(first_table[j, 1])
        angle_1: float = get_angle_axe_x(x1, y1)

        for i in range(j, n_peaks):

            y2 = int(first_table[i, 0])
            x2 = int(first_table[i, 1])
            angle_2: float = get_angle_axe_x(x2, y2)

            peaks_angle: int = int(angle_2 - angle_1)

            peaks_angle_abs: int = abs(peaks_angle)
            if ((peaks_angle_abs < cfg.angle_min) or
                    (peaks_angle_abs > cfg.angle_max)):
                continue

            second_table[n_rows, 0] = y1
            second_table[n_rows, 1] = x1
            second_table[n_rows, 2] = y2
            second_table[n_rows, 3] = x2
            second_table[n_rows, 4] = peaks_angle

            n_rows += 1

    return second_table, n_rows
