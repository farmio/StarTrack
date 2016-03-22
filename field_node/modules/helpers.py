from threading import Thread
from time import sleep


class Delegate(object):
    """ Delegate class enables functions to add and remove callbacks. """
    # thanks to kindall on stackoverflow.com
    def __init__(self, func):
        self.callbacks = []
        self.basefunc = func

    def __iadd__(self, func):
        """ Adds `func` to `self.callbacks`. """
        if callable(func):
            self.__isub__(func)
            self.callbacks.append(func)
        return self

    def callback(self, func):
        """ Adds `func` to `self.callbacks`. Returns `func`. """
        if callable(func):
            self.__isub__(func)
            self.callbacks.append(func)
        return func

    def __isub__(self, func):
        """ Removes `func` from `self.callbacks`. """
        try:
            self.callbacks.remove(func)
        except ValueError:
            pass
        return self

    def clear(self):
        """ Removes everything from `self.callbacks` leaving self.basefunc. """
        for func in self.callbacks:
            self.callbacks.remove(func)

    def __call__(self, *args, **kwargs):
        result = self.basefunc(*args, **kwargs)
        for func in self.callbacks:
            # print('args: ', args)
            newresult = func(result)
            result = result if newresult is None else newresult
        return result


class Queue(Thread):
    def __init__(self, func, q, pause=0):
        """
        `func` is called when `q` threading.Lock() instance is released and
        sleeps for `pause` seconds
        """
        self.func = func
        self.queue = q
        self.pause = pause
        Thread.__init__(self)

    def run(self):
        self.queue.acquire()
        self.func()
        sleep(self.pause)
        self.queue.release()


class Timer(Thread):
    """ Timer class. Spawns a new thread. """
    def __init__(self, delay, func):
        """
        `func(self)` is called every `delay` seconds
        Start with self.start()
        """
        self.delay = delay
        self.func = func
        Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        sleep(self.delay)
        self.func()


class Infinite_Timer(Timer):
    """ Infinite timer class. Spawns a new thread. """
    def __init__(self, delay, func):
        """
        `func()` is called every `delay` seconds
        Start with self.start()
        """
        self.stop = False
        super(Infinite_Timer, self).__init(self, delay, func)

    def kill(self):
        """ Stops timer - ends thread before next update. """
        self.stop = True

    def run(self):
        while True:
            if self.stop:
                return
            else:
                self.func()
                sleep(self.delay)


class Resettable_Timer(Thread):
    """ Resettable timer class. Spawns a new thread. """
    def __init__(self, maxtime, expire, step=None, update=None):
        """
        `update(self)` is called every `step` seconds
        until `maxtime` in seconds is reached.
        step default is 'maxtime'/2
        `expire(self)` is called at maxtime.
        Start with self.start()
        """
        self.maxtime = maxtime
        self.expire = expire
        if step:
            self.step = step
        else:
            self.step = maxtime / 2
        if update:
            self.update = update
        else:
            self.update = lambda c: None
        self.counter = 0
        self.active = True
        self.stop = False
        Thread.__init__(self)
        self.setDaemon(True)

    def set_counter(self, t):
        """ Sets self.counter to `t`. """
        self.counter = t

    def deactivate(self):
        """ Deactivates call of update and expire function. """
        self.active = False

    def kill(self):
        """ Stops timer - ends thread before next update. """
        self.stop = True

    def reset(self):
        """ Resets and activates timer. """
        self.counter = 0
        self.active = True

    def run(self):
        while True:
            self.counter = 0
            while self.counter < self.maxtime:
                self.counter += self.step
                sleep(self.step)
                if self.stop:
                    return
                if self.active:
                    self.update()
            if self.active:
                self.expire()
                self.active = False
