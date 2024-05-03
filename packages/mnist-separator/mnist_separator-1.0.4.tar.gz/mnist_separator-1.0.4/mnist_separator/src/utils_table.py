# May-02-2024
# utils_table.py

from numpy import ndarray


def save_table(tag, directory, table: ndarray, n_rows: int, n_cols: int):

    data_path = directory + '/' + tag + '.txt'

    with open(data_path, 'w') as fp:

        for j in range(n_rows):
            # fp.write(f'{j}:\t\t')
            for i in range(n_cols):
                fp.write(f'{table[j, i]}\t\t')
            fp.write(f'\n')
