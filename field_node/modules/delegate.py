import threading
from time import sleep

#thanks to kindall on stackoverflow.com
class Delegate(object):

    def __init__(self, func):
        self.callbacks = []
        self.basefunc = func

    def __iadd__(self, func):
        if callable(func):
            self.__isub__(func)
            self.callbacks.append(func)
        return self

    def callback(self, func):
        if callable(func):
            self.__isub__(func)
            self.callbacks.append(func)
        return func

    def __isub__(self, func):
        try:
            self.callbacks.remove(func)
        except ValueError:
            pass
        return self

    def __call__(self, *args, **kwargs):
        result = self.basefunc(*args, **kwargs)
        for func in self.callbacks:
            newresult = func(result)
            result = result if newresult is None else newresult
        return result


class Queue(threading.Thread):
    def __init__(self, func, q, rest=0):
        threading.Thread.__init__(self)
        if callable(func):          #this isn't good
            self.func = func
            self.queue = q
            self.rest = rest
        else:
            print 'Queue needs function and threading.Lock() instance'

    def run(self):
        self.queue.acquire()
        self.func()
        sleep(self.rest)
        self.queue.release()
