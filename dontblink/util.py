import string
import random
from datetime import datetime


PALETTE = string.ascii_letters + string.digits


def random_string(length):
    global PALETTE
    return ''.join([random.choice(PALETTE) for _ in range(length)])


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    print(random_string(120))
    print(now())
