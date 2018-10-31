#!/usr/bin/env python

import time

from datetime import datetime
from multiprocessing import Process

def foo(value: int, delay: int):

    time.sleep(delay)

    print(value)


if __name__ == '__main__':

    print('===== About to start the wall clock test ======')

    processes = [
        Process(target=foo, args=(i, i)) for i in range(3)
    ]

    print(f'About to start: {datetime.now()}')

    for process in processes:
        process.start()
        process.join()

    print(f'About to finish: {datetime.now()}')

    print("===== About to start the print sequence test =====")

    processes = [
        Process(target=foo, args=(i, 0)) for i in range(50)
    ]

    for process in processes:
        process.start()
        process.join()
