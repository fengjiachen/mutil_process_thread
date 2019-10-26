import concurrent
from concurrent.futures import ProcessPoolExecutor


class MyProcessPoolExecutor(object):
    def __init__(self):
        self.data = [1, 2, 3, 4]

    def worker(self, data=None):
        print('process data', data)
        return data*10

    def runner(self):
        process_pool = ProcessPoolExecutor(max_workers=4)
        futures = dict()
        for d in self.data:
            future = process_pool.submit(self.worker, d)
            futures[future] = d

        for future in concurrent.futures.as_completed(futures):
            d = futures[future]
            print('data {} turn to the result {}'.format(d, future.result()))
        print('Finished!')


if __name__ == '__main__':
    MyProcessPoolExecutor().runner()
