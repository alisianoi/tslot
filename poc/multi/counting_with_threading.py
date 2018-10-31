#!/usr/bin/env python

from threading import Thread, Lock

i = 0

def foo(lock: Lock, name: int):
    global i

    lock.acquire()

    i += 1

    print(f'This is thread {name} with counter {i}')

    lock.release()


if __name__ == '__main__':

    lock = Lock()

    threads = [Thread(target=foo, args=(lock, i)) for i in range(10)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
