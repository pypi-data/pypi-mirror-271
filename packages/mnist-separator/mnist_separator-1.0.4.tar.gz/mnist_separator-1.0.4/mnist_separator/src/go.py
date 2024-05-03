# May-02-2024
# go.py

import sys
import os
import numpy as np
import random
from tqdm import tqdm

from mnist_separator.src import glbl
from mnist_separator.src.timer import init_timer, save_elapsed_time_hour_min_sec
from mnist_separator.src.convert_data import convert_data
from mnist_separator.src.get_similarity_group import get_similarity_group
from mnist_separator.src.utils_list import list_visible_files
from mnist_separator.src.save_result import save_result


def go():

    init_timer()

    convert_data()

    list_result_0 = []
    list_result_1 = []
    list_result_2 = []
    list_result_3 = []
    list_result_4 = []
    list_result_5 = []
    list_result_6 = []
    list_result_7 = []
    list_result_8 = []
    list_result_9 = []

    list_test_files = []
    list_test_files_conon = list_visible_files(glbl.path_test_canon)
    for fname in list_test_files_conon:
        path_test_canon = glbl.path_test_canon + '/' + fname
        list_test_files.append(path_test_canon)

    random.shuffle(list_test_files)
    n_test_files = len(list_test_files)
    if n_test_files == 0:
        sys.exit(f'\nNo data')

    print()
    for n in tqdm(range(n_test_files), desc='separation'):

        path_test_canon = list_test_files[n]

        list_similarities = [get_similarity_group(path_test_canon, glbl.path_train_0_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_1_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_2_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_3_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_4_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_5_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_6_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_7_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_8_canon),
                             get_similarity_group(path_test_canon, glbl.path_train_9_canon)]

        name_test = os.path.basename(path_test_canon)
        index = np.argmax(list_similarities)

        match index:
            case 0: list_result_0.append(name_test)
            case 1: list_result_1.append(name_test)
            case 2: list_result_2.append(name_test)
            case 3: list_result_3.append(name_test)
            case 4: list_result_4.append(name_test)
            case 5: list_result_5.append(name_test)
            case 6: list_result_6.append(name_test)
            case 7: list_result_7.append(name_test)
            case 8: list_result_8.append(name_test)
            case 9: list_result_9.append(name_test)

    save_result(list_result_0, list_result_1,
                list_result_2, list_result_3,
                list_result_4, list_result_5,
                list_result_6, list_result_7,
                list_result_8, list_result_9)

    save_elapsed_time_hour_min_sec(glbl.result_name)
