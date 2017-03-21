from contextlib import contextmanager


@contextmanager
def patch(obj, *delattrs, **setattrs):
    """Monkey-patch an object, then restore its original attributes."""
    added = object()
    originals = {}
    try:
        for name in delattrs:
            originals[name] = getattr(obj, name)
            delattr(obj, name)
        for name, value in setattrs.items():
            originals[name] = getattr(obj, name, added)
            setattr(obj, name, value)
        yield
    finally:
        for name, value in originals.items():
            if value is added:
                delattr(obj, name)
            else:
                setattr(obj, name, value)


@contextmanager
def redefine(func, new_func):
    """Redefine func to behave like new_func.

    All references to func -- even those in other scopes or modules --
    will exhibit the new behavior until this context manager exits.
    """
    original_code = func.__code__
    func.__code__ = new_func.__code__
    try:
        yield
    finally:
        func.__code__ = original_code
    # alternatively: patch(func, __code__=new_func.__code__)


def instrument(func, decorator):
    """Remotely decorate func with decorator within this context manager."""
    return redefine(func, decorator(func))
    # alternatively: patch(func, __code__=decorator(func).__code__)
