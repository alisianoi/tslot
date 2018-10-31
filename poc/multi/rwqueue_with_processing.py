#!/usr/bin/env python

from multiprocessing import Process, Queue

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

    processes = [
        Process(target=foo, args=(queue,))
        , Process(target=bar, args=(queue,))
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
