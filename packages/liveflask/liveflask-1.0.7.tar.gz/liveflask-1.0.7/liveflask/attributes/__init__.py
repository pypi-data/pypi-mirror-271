import functools


def url(arg: list | None = None):
    def decorator(cls):
        @functools.wraps(cls, updated=())
        class DecoratedClass(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.__class__.__name__ = cls.__name__

        cls.mvlive__url = []

        if arg is not None:
            for query_param in arg:
                # Assuming Request.input() does something meaningful
                # Here, we attach the result of Request.input() to the class
                cls.mvlive__url.append(query_param)
        return DecoratedClass

    return decorator


def locked(arg: list | None = None):
    def decorator(cls):
        @functools.wraps(cls, updated=())
        class DecoratedClass(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.__class__.__name__ = cls.__name__

        cls.mvlive__locked = []

        if arg is not None:
            for locked_prop in arg:
                # Assuming Request.input() does something meaningful
                # Here, we attach the result of Request.input() to the class
                cls.mvlive__locked.append(locked_prop)
        return DecoratedClass

    return decorator


def session(arg: list | None = None):
    def decorator(cls):
        @functools.wraps(cls, updated=())
        class DecoratedClass(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.__class__.__name__ = cls.__name__

        cls.mvlive__session = []

        if arg is not None:
            for session_binded_prop in arg:
                # Assuming Request.input() does something meaningful
                # Here, we attach the result of Request.input() to the class
                cls.mvlive__session.append(session_binded_prop)
        return DecoratedClass

    return decorator
