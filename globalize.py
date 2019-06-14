import builtins
import importlib
import sys
# __globals__ = __builtins__.globals
# __globals__ = globals()


def get_or_import(dct, name):
    print(f"*** getting {name}")
    try:
        return dct[name]
    except KeyError:
        print(f"*** missing {name}")
        try:
            module = importlib.import_module(name)
        except ImportError:
            print(f"*** failed to import {name}")
            raise AttributeError(name)
        else:
            print(f"*** successfully imported {name}")
            dct[name] = module
            print(f"*** returning {name}")
            return module


class Base:
    def __init__(self, dct):
        self._dct = dct

    def __getattr__(self, name):
        return get_or_import(self._dct, name)


base = Base(globals())


class ImportDict(dict):

    def __missing__(self, name):
        print(f"*** missing {name}")
        try:
            module = importlib.import_module(name)
        except ImportError:
            print(f"*** failed to import {name}")
            raise KeyError(name)
        print(f"*** successfully imported {name}")
        self[name] = module
        print(f"*** returning {name}")
        return module


# # def globals():
# #     print('*** accessing globals')
# #     return ImportDict(__globals__)


# builtins.__globals__ = builtins.globals()


assert (
    globals
    is builtins.globals
    is __builtins__['globals']
)

assert (
    globals()
    is builtins.globals()
    is __builtins__['globals']()
)

builtins.__globals__ = globals()

assert (
    __globals__  # noqa
    is globals()
    is builtins.globals()
    is builtins.__globals__
    is __builtins__['globals']()
    is __builtins__['__globals__']
)

importer = ImportDict(globals())

builtins.globals = lambda: importer

assert globals() is not __globals__  # noqa
assert globals() is importer

# __builtins__ = importer


class Test(type(builtins)):
    def __getattr__(self, name):
        print(f"*** getting {name}")
        try:
            return importer[name]
        except KeyError:
            print(f"*** failed to get {name}")
            raise AttributeError(name)


sys.modules['builtins'] = Test('builtins')


# print(atomic)
