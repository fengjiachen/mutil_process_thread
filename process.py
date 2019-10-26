import time
import datetime
import traceback
from multiprocessing import Process, Queue


class Worker(Process):
    def __init__(self, in_queue, out_queue):
        super(Worker, self).__init__()

        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        try:
            num = self.in_queue.get()
            """
            do your task
            """
            # workers can read the same file
            msg = 'task {} finished at {}'.format(
                num, datetime.datetime.now())
            print(msg)
            self.out_queue.put(msg)
        except:
            print(traceback.format_exc())


class Collector(Process):
    def __init__(self, out_queue, num):
        super(Collector, self).__init__()
        self.collect_num = num
        self.out_queue = out_queue

    def run(self):
        while self.collect_num > 0:
            result = self.out_queue.get()
            line = 'collected at {}'.format(datetime.datetime.now())
            print(line)
            self.collect_num -= 1


if __name__ == '__main__':
    print('start')
    in_queue = Queue()
    out_queue = Queue()
    work_num = 4
    col = Collector(out_queue, work_num)
    col.start()
    worker_list = []
    for i in range(work_num):
        worker = Worker(in_queue, out_queue)
        worker_list.append(worker)
        worker.start()
    """
    dispatch your work
    """
    print('dispatch')
    for i in range(work_num):
        in_queue.put(i)

    print('start to work')
    while not in_queue.empty():
        print('still working')
        time.sleep(1)

    print('start to collect result')
    while not out_queue.empty():
        print('still collect result')
        time.sleep(1)
    print('wait for finish')
    time.sleep(5)
    exit()
