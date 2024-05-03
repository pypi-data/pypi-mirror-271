# May-02-2024
# sort_peaks.py

import numpy as np

from mnist_separator.src.shell_sort import shell_sort_decrease


def sort_peaks(magn, list_in):

    len_list = len(list_in)
    arr_magn = np.zeros(len_list, dtype=np.float32)

    n = 0
    for item in list_in:
        y = int(item[0])
        x = int(item[1])

        arr_magn[n] = magn[y, x]
        n += 1

    # Сортировка arr_magn.
    order = np.arange(len_list)
    shell_sort_decrease(arr_magn, order, len_list)

    # Пики в списке list_out отсортированы по значению магнитуды.
    list_out = []
    for i in range(len_list):
        j = order[i]
        item = list_in[j]
        list_out.append(item)

    return list_out
