# May-02-2024
# shell_sort.py


# vect1: 1, 2, 3, ...
def shell_sort_increase(vect1, vect2, n):

    gap = n // 2

    while gap > 0:

        for i in range(gap, n):

            j = i - gap

            while j >= 0 and vect1[j] > vect1[j+gap]:

                temp = vect1[j]
                vect1[j] = vect1[j+gap]
                vect1[j+gap] = temp

                temp = vect2[j]
                vect2[j] = vect2[j+gap]
                vect2[j+gap] = temp

                j = j - gap

        gap = gap // 2


# vect1: 3, 2, 1, ...
def shell_sort_decrease(vect1, vect2, n):

    gap = n // 2

    while gap > 0:

        for i in range(gap, n):

            j = i - gap

            while j >= 0 and vect1[j] < vect1[j + gap]:
                temp = vect1[j]
                vect1[j] = vect1[j + gap]
                vect1[j + gap] = temp

                temp = vect2[j]
                vect2[j] = vect2[j + gap]
                vect2[j + gap] = temp

                j = j - gap

        gap = gap // 2
