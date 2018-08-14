from functools import wraps
import signal


def upload_file(file, dirname=''):
    path = f'/{dirname}/' + file.name
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


class TimeoutError(Exception): pass


def timeout(seconds, error_message='Function call timed out'):
    def handler_timeout(signum, frame):
        raise TimeoutError(error_message)

    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorated
