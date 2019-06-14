import builtins
import importlib
import sys
# __globals__ = __builtins__.globals
# __globals__ = globals()


# class Base:
#     # TODO: extend ModuleType?
#     def __init__(self, vars):
#         self._vars = vars

#     def __getattr__(self, name):
#         try:
#             return self._vars[name]
#         except KeyError:
#             print(f"*** missing {name}")
#             try:
#                 module = importlib.import_module(name)
#             except ImportError:
#                 print(f"*** failed to import {name}")
#                 raise AttributeError(name)
#             else:
#                 print(f"*** successfully imported {name}")
#                 self._vars[name] = module
#                 print(f"*** returning {name}")
#                 return module

# # base = Base(globals())


# sys.modules[__name__] = Base(vars(builtins))


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


class ImportDict(dict):
    """yolo"""

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


# TODO: implement Base via a metaclass/type using an ImportDict


class Base:
    def __init__(self, dct):
        self.__dict = ImportDict(dct)

    def __getattr__(self, name):
        return self.__dict[name]


# base = Base(ImportDict(vars(builtins)))
sys.modules['builtins'] = Base(vars(builtins))


# class Base:
#     def __init__(self, dct):
#         self.__dict__ = dct

#     def __getattr__(self, name):
#         return get_or_import(self.__dict__, name)


# base = Base(globals())
