# May-02-2024
# timer.py

import time
from pathlib import Path
from datetime import date, datetime

global timer_start


def init_timer():
    global timer_start
    timer_start = time.time()


def save_elapsed_time_hour_min_sec(dir_name: str):
    global timer_start

    today = date.today()
    current_date = today.strftime("%B %d, %Y")
    c = datetime.now()
    current_time = c.strftime('%H:%M:%S')
    when = current_date + '\t' + current_time

    timer_end = time.time()
    seconds = int(timer_end - timer_start)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    fname = Path.cwd() / dir_name / "date_time.txt"
    with open(fname, 'w') as fname:
        str_time = f'{h:02d} hour(s)  {m:02d} min  {s:02d} sec'
        fname.write(when + '\n\n')
        fname.write('Elapsed time = ' + str_time + '\n')
