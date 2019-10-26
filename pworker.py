import datetime
import time
import traceback
import multiprocessing
from multiprocessing import Process, Queue


class Worker(Process):
    def __init__(self, in_queue, out_queue):
        super(Worker, self).__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        try:
            data = self.in_queue.get()
            msg = 'task {} finished at {}'.format(
                data, datetime.datetime.now())
            print(msg)
            self.out_queue.put(data)
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
            line = 'collected {} at {}'.format(result, datetime.datetime.now())
            print(line)
            self.collect_num -= 1
        print('collect finish')


if __name__ == '__main__':
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

    worker_list.append(col)

    """
    dispatch your work
    """
    print('dispatch')
    for i in range(work_num):
        in_queue.put(i)
    for wl in worker_list:
        wl.join()
    print('main process exit')
