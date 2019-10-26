from datetime import datetime
from queue import Queue
from random import randint
from threading import Thread
from time import sleep
'''
多线程工作流
'''


class ThreadingWorker(object):
    def __init__(self):
        self.queue = Queue(2)

    def collect(self, num):
        for i in range(num):
            result = self.queue.get(block=1)
            print('collect {} result {}'.format(i, result))

    def worker(self, data):
        line = 'work {} start at {}'.format(data, datetime.now())
        print(line)
        self.queue.put(data, block=1)

    def go(self):
        print('ThreadingWorker Start!')
        num_work = 5
        threads = []
        for i in range(num_work):
            thread = Thread(target=self.worker, args=(i,))
            thread.start()
            threads.append(thread)
        thread = Thread(target=self.collect, args=(num_work,))
        thread.start()
        threads.append(thread)
        for thread in threads:
            thread.join()
        print('ThreadingWorker Done!')


if __name__ == '__main__':
    ThreadingWorker().go()
