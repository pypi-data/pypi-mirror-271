# May-02-2024
# calc_similarity.py

import numpy as np

from mnist_separator.src.magnitude import get_magn_roi, get_magn_half
from mnist_separator.src.get_peaks import get_peaks
from mnist_separator.src.sort_peaks import sort_peaks
from mnist_separator.src.utils_list_of_peaks import cut_list_of_peaks
from mnist_separator.src.calc_similarity_2pnts import calc_similarity_2pnts
from mnist_separator.src.calc_similarity_3pnts import calc_similarity_3pnts


def calc_similarity(image: np.uint8, templ: np.uint8) -> float:

    # Image
    # ---------------------------------------------------------
    image_magn_roi = get_magn_roi(image)
    image_magn_half = get_magn_half(image_magn_roi)

    image_list_of_peaks = get_peaks(image_magn_half)
    image_list_of_peaks_sort = sort_peaks(image_magn_half, image_list_of_peaks)
    image_list_of_peaks_calc = cut_list_of_peaks(image_list_of_peaks_sort)
    # ---------------------------------------------------------

    # Templ
    # ---------------------------------------------------------
    templ_magn_roi = get_magn_roi(templ)
    templ_magn_half = get_magn_half(templ_magn_roi)

    templ_list_of_peaks = get_peaks(templ_magn_half)
    templ_list_of_peaks_sort = sort_peaks(templ_magn_half, templ_list_of_peaks)
    templ_list_of_peaks_calc = cut_list_of_peaks(templ_list_of_peaks_sort)
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    similarity_result_2pnts = calc_similarity_2pnts(
                                        image_magn_roi, templ_magn_roi,
                                        image_list_of_peaks_calc,
                                        templ_list_of_peaks_calc)

    similarity_result_3pnts = calc_similarity_3pnts(
                                        image_magn_roi, templ_magn_roi,
                                        image_list_of_peaks_calc,
                                        templ_list_of_peaks_calc)
    # ---------------------------------------------------------

    return max(similarity_result_2pnts, similarity_result_3pnts)
