import concurrent.futures
import threading


class Fut:
    def __init__(self, max_workers=8):
        self.futures = []
        self.values = []
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.value_count = -1

    def set_func(self, func):
        self.func = func

    def append(self, value):
        if not self.func:
            raise RuntimeError("Set function through set_func member")
        self.futures.append(self.executor.submit(self.wrapper, value))

    def wrapper(self, *args, **kwargs):
        self.value_count += 1
        return (self.value_count, self.func(*args, **kwargs))

    def result_ordered(self):
        res = []
        for fut in concurrent.futures.as_completed(self.futures):
            res.append(fut.result())
        for _, value in sorted(res, key=lambda x: x[0]):
            yield value


    def result(self):
        for fut in concurrent.futures.as_completed(self.futures):
            indx, value = fut.result()
            yield value


def Main():
    obj = Fut()
    obj.set_func(lambda x: x*x + 2*x +13)
    for i in range(10):
        obj.append(i)

    for result in obj.result_ordered():
        print(result)


if __name__ == '__main__':
   Main()
