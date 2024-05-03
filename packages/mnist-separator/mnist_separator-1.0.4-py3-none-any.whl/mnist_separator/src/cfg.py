# May-02-2024
# cfg.py

path_image: str = ''
path_templ: str = ''

# Число локальных максимумов в
# верхней полуплоскости.
n_peaks: int = 9

size_dft: int = 2048
lp_param: int = 4
size_roi: int = size_dft // lp_param
dsize_roi = (size_roi, size_roi)
size_roi_half: int = size_roi // 2
X0: int = size_roi_half
Y0: int = size_roi_half
center = (X0, Y0)

angle_min: int = 20
angle_max: int = 180 - angle_min
angle_ratio_threshold: float = 3.0

param_similarity: float = 0.07

y1_image: int = -1
x1_image: int = -1
y2_image: int = -1
x2_image: int = -1

y1_templ: int = -1
x1_templ: int = -1
y2_templ: int = -1
x2_templ: int = -1
