import random

from time import sleep
from datetime import datetime


def randomized_sleep(average=1):
    _min, _max = average * 1 / 2, average * 3 / 2
    sleep(random.uniform(_min, _max))


def today_datetime():
    return datetime.today().strftime('%Y%m%d%H%M%S')
