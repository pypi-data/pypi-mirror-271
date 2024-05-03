# May-02-2024
# save_result.py

from mnist_separator.src import glbl
from mnist_separator.src.utils_list import save_list


def save_result(list_result_0, list_result_1,
                list_result_2, list_result_3,
                list_result_4, list_result_5,
                list_result_6, list_result_7,
                list_result_8, list_result_9):

    if len(list_result_0) > 0:
        save_list('list_result_0.txt', glbl.result_name, list_result_0)
    if len(list_result_1) > 0:
        save_list('list_result_1.txt', glbl.result_name, list_result_1)
    if len(list_result_2) > 0:
        save_list('list_result_2.txt', glbl.result_name, list_result_2)
    if len(list_result_3) > 0:
        save_list('list_result_3.txt', glbl.result_name, list_result_3)
    if len(list_result_4) > 0:
        save_list('list_result_4.txt', glbl.result_name, list_result_4)
    if len(list_result_5) > 0:
        save_list('list_result_5.txt', glbl.result_name, list_result_5)
    if len(list_result_6) > 0:
        save_list('list_result_6.txt', glbl.result_name, list_result_6)
    if len(list_result_7) > 0:
        save_list('list_result_7.txt', glbl.result_name, list_result_7)
    if len(list_result_8) > 0:
        save_list('list_result_8.txt', glbl.result_name, list_result_8)
    if len(list_result_9) > 0:
        save_list('list_result_9.txt', glbl.result_name, list_result_9)
