import concurrent
from concurrent.futures import ThreadPoolExecutor


class MyThreadPoolExecutor(object):
    def __init__(self):
        self.data = [1, 2, 3, 4]

    def worker(self, data=None):
        print('process data', data)
        return data*10

    def runner(self):
        thread_pool = ThreadPoolExecutor(
            max_workers=2, thread_name_prefix='work')
        futures = dict()
        for d in self.data:
            future = thread_pool.submit(self.worker, d)
            futures[future] = d

        for future in concurrent.futures.as_completed(futures):
            d = futures[future]
            print('data {} turn to the result {}'.format(d, future.result()))
        print('Finished!')


if __name__ == '__main__':
    MyThreadPoolExecutor().runner()
