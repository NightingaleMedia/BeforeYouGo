from threading import Thread

def threaded(fn):
    def wrapper(*args, **kwargs):
        print('theading the func...')
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper