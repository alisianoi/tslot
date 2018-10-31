#!/usr/bin/env python

from queue import Queue
from threading import Thread

def foo(queue: Queue):

    for i in range(10):
        print('getter is up')
        print(queue.get())

def bar(queue: Queue):

    for i in range(10):
        print('putter is up')
        queue.put(i)

if __name__ == '__main__':

    queue = Queue(maxsize=1)

    threads = [
        Thread(target=foo, args=(queue,)), Thread(target=bar, args=(queue,))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
