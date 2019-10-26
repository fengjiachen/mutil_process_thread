import multiprocessing
from multiprocessing import Process

# a mutilprocessing sample

class LockProcess(Process):
    def __init__(self, name=None, lock=None, m_count=None):
        Process.__init__(self, name=name)
        self.lock = lock
        self.m_count = m_count

    def run(self):
        self.lock.acquire()
        print('process is '+multiprocessing.current_process().name+', lock acquired!')
        # 性能问题，100000次循环，所以这里优化为先从多进程共享拿出来计算完再放回多进程共享
        count = self.m_count.value
        for i in range(0, 100):
            count += 1
        self.m_count.value = count
        print('process is '+multiprocessing.current_process().name +
              ', pre lock release!')
        self.lock.release()


if __name__ == '__main__':
    processes = list()
    lock = multiprocessing.Lock()
    m_count = multiprocessing.Manager().Value('count', 0)

    for i in range(0, 10):
        process = LockProcess(name=str(i), lock=lock, m_count=m_count)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
    print('Main Process finish, LockProcess.count is:' + str(m_count.value))
