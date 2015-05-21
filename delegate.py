import threading

#thanks to kindall on stackoverflow.com

class delegate(object):

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

    def callback_async(self, func):
        if callable(func):
            self.__isub__(func)
            self.callbacks.append(lambda x:
                threading.Thread(target=func).start()
                )

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
