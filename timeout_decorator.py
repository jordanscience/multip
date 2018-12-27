from threading import Thread
import functools
import os


def timeout(timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]

            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    pass

            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                print('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                if func.__name__ == 'exercice':
                    print(" \n Temps limite dépassé ! \n GAME OVER")
                    os._exit(1)
                elif func.__name__ == 'question':
                    raise TimeoutError()
                # raise ret
            return ret

        return wrapper

    return deco
