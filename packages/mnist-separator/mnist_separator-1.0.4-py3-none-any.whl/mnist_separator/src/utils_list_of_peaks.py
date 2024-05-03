# May-02-2024
# utils_list_of_peaks.py

from mnist_separator.src import cfg


def cut_list_of_peaks(list_of_peaks) -> list:

    # remove first peak
    list_of_peaks_1 = list_of_peaks[1:]

    length = len(list_of_peaks_1)

    if length > cfg.n_peaks:
        # remove extra peaks from the end
        list_of_peaks_1 = list_of_peaks_1[:cfg.n_peaks]

    return list_of_peaks_1


def save_list_of_peaks(tag, directory, magn, list_of_peaks):

    data_path = directory + '/' + tag + '.txt'

    with open(data_path, 'w') as fp:
        n: int = 0
        for item in list_of_peaks:
            y = item[0]
            x = item[1]
            fp.write(f'{n}:\t {item}\t magn = {magn[y, x]}\n')
            n += 1


def save_list_of_peaks_1(tag, directory, list_of_peaks):

    data_path = directory + '/' + tag + '.txt'

    with open(data_path, 'w') as fp:
        n: int = 0
        for item in list_of_peaks:
            fp.write(f'{n}:\t {item}\n')
            n += 1


def read_list_of_peaks_1(tag, directory):

    list_of_peaks = []

    data_path = directory + '/' + tag + '.txt'

    with open(data_path, 'r') as fp:
        for line in fp:

            # remove linebreak from a current item
            item = line[:-1]

            list_of_peaks.append(item)

    return list_of_peaks
