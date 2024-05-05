import inspect
from typing import Type


class NotImplementedMethodError(Exception):
    def __init__(self, function_name: str = ''):
        message = f"Method {function_name} is not implemented."
        super().__init__(message)


def todo():
    """
    替代pass，避免被忽略
    :return:
    """
    current_frame = inspect.currentframe()
    parent_frame = current_frame.f_back
    parent_function_name: str = parent_frame.f_code.co_name
    raise NotImplementedMethodError(parent_function_name)


def no_error(throw: callable = print,
             format: str = "Error: {}",
             errors: tuple | Type[Exception] = Exception):
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                throw(format.format(e))
        return inner
    return wrapper


if __name__ == '__main__':
    @no_error(print, "Error: {}", Exception)
    def test():
        print("test")
    test()
