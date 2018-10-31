#!/usr/bin/env python

import time

from datetime import datetime
from threading import Thread

def foo(value: int, delay: int):

    time.sleep(delay)

    print(value)


if __name__ == '__main__':

    print('===== About to start the wall clock test ======')

    threads = [
        Thread(target=foo, args=(i, i)) for i in range(3)
    ]

    print(f'About to start: {datetime.now()}')

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f'About to finish: {datetime.now()}')

    print("===== About to start the print sequence test =====")

    threads = [
        Thread(target=foo, args=(i, 0)) for i in range(50)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
