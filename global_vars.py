# Experiments with global vars and builtins.

# globals() is always cached
assert globals() is globals()

# globals() is always a dict
assert isinstance(globals(), dict)

if __spec__ is None:  # This file was run via `python global_vars.py`.
    assert dir() == [
        '__annotations__',
        '__builtins__',
        '__cached__',
        '__doc__',
        '__file__',
        '__loader__',
        '__name__',
        '__package__',
        '__spec__',
    ], dir()
    exit()

elif __name__ == '__main__':  # This file was run via `python -m global_vars`.
    print(f"__main__")

    assert dir() == [
        '__annotations__',
        '__builtins__',
        '__cached__',
        '__doc__',
        '__file__',
        '__loader__',
        '__name__',
        '__package__',
        '__spec__',
    ], dir()

    assert __annotations__ == {}, __annotations__

    # We'll get to __builtins__ later.

    print(f"__cached__: {__cached__}")  # noqa

    assert __doc__ is None, __doc__

    print(f"__file__: {__file__}")

    assert __loader__.__class__.__name__ == 'SourceFileLoader'
    assert __loader__.__class__.__module__ == '_frozen_importlib_external'
    print(f"__loader__.name: {__loader__.name}")
    assert __loader__.name == __spec__.name
    assert __loader__.path == __file__, __loader__.path

    assert __package__ == '', __package__
    print(f"__spec__: {__spec__}")
    assert __spec__.name == __loader__.name
    assert __spec__.__class__.__name__ == 'ModuleSpec'
    assert __spec__.__class__.__module__ == '_frozen_importlib'
    assert __spec__.loader is __loader__
    assert __spec__.cached == __cached__  # noqa
    # import pdb; pdb.set_trace()

    # `__builtins__` is an alias for the `builtins` module
    assert __builtins__.__class__.__name__ == 'module'
    assert __builtins__.__name__ == 'builtins'
    assert __builtins__.__package__ == ''
    assert __builtins__.__spec__.name == 'builtins'
    assert __builtins__.__doc__ == (
        "Built-in functions, exceptions, and other objects."
        "\n\n"
        "Noteworthy: None is the `nil' object;"
        " Ellipsis represents `...' in slices."
    )

    assert dir() == sorted(globals()), (dir(), sorted(globals()))

    # TODO: ???
    assert __build_class__.__module__ == 'builtins', __build_class__.__module__

    # TODO: what are all these tab completions?
    # >>> __
    # __annotations__   __cached__        __doc__           __loader__        __package__
    # __build_class__(  __debug__         __import__(       __name__          __spec__

    assert len(globals()) == 9, len(globals())
    assert len(dir(__builtins__)) == 152, len(dir(__builtins__))

    assert dir(__builtins__) == sorted(vars(__builtins__))
    # assert sorted(vars(__builtins__)) == dir(__builtins__)

    assert (
        len(globals().keys() - dir(__builtins__)) == 4
    ), globals().keys() - dir(__builtins__)

    assert (
        len(vars(__builtins__).keys() - globals()) == 147
    ), len(vars(__builtins__).keys() - globals())

    assert globals().keys() - dir(__builtins__) == {
            '__annotations__',
            '__cached__',
            '__file__',
            '__builtins__',
    }, globals().keys() - dir(__builtins__)

    assert globals().keys() == {
        '__name__',
        '__doc__',
        '__package__',
        '__loader__',
        '__spec__',
        '__annotations__',
        '__builtins__',
        '__file__',
        '__cached__',
    }, globals().keys()

    assert vars(__builtins__).keys() == {
        '__name__',
        '__doc__',
        '__package__',
        '__loader__',
        '__spec__',
        '__build_class__',
        '__import__',
        'abs',
        'all',
        'any',
        'ascii',
        'bin',
        'breakpoint',
        'callable',
        'chr',
        'compile',
        'delattr',
        'dir',
        'divmod',
        'eval',
        'exec',
        'format',
        'getattr',
        'globals',
        'hasattr',
        'hash',
        'hex',
        'id',
        'input',
        'isinstance',
        'issubclass',
        'iter',
        'len',
        'locals',
        'max',
        'min',
        'next',
        'oct',
        'ord',
        'pow',
        'print',
        'repr',
        'round',
        'setattr',
        'sorted',
        'sum',
        'vars',
        'None',
        'Ellipsis',
        'NotImplemented',
        'False',
        'True',
        'bool',
        'memoryview',
        'bytearray',
        'bytes',
        'classmethod',
        'complex',
        'dict',
        'enumerate',
        'filter',
        'float',
        'frozenset',
        'property',
        'int',
        'list',
        'map',
        'object',
        'range',
        'reversed',
        'set',
        'slice',
        'staticmethod',
        'str',
        'super',
        'tuple',
        'type',
        'zip',
        '__debug__',
        'BaseException',
        'Exception',
        'TypeError',
        'StopAsyncIteration',
        'StopIteration',
        'GeneratorExit',
        'SystemExit',
        'KeyboardInterrupt',
        'ImportError',
        'ModuleNotFoundError',
        'OSError',
        'EnvironmentError',
        'IOError',
        'EOFError',
        'RuntimeError',
        'RecursionError',
        'NotImplementedError',
        'NameError',
        'UnboundLocalError',
        'AttributeError',
        'SyntaxError',
        'IndentationError',
        'TabError',
        'LookupError',
        'IndexError',
        'KeyError',
        'ValueError',
        'UnicodeError',
        'UnicodeEncodeError',
        'UnicodeDecodeError',
        'UnicodeTranslateError',
        'AssertionError',
        'ArithmeticError',
        'FloatingPointError',
        'OverflowError',
        'ZeroDivisionError',
        'SystemError',
        'ReferenceError',
        'MemoryError',
        'BufferError',
        'Warning',
        'UserWarning',
        'DeprecationWarning',
        'PendingDeprecationWarning',
        'SyntaxWarning',
        'RuntimeWarning',
        'FutureWarning',
        'ImportWarning',
        'UnicodeWarning',
        'BytesWarning',
        'ResourceWarning',
        'ConnectionError',
        'BlockingIOError',
        'BrokenPipeError',
        'ChildProcessError',
        'ConnectionAbortedError',
        'ConnectionRefusedError',
        'ConnectionResetError',
        'FileExistsError',
        'FileNotFoundError',
        'IsADirectoryError',
        'NotADirectoryError',
        'InterruptedError',
        'PermissionError',
        'ProcessLookupError',
        'TimeoutError',
        'open',
        'quit',
        'exit',
        'copyright',
        'credits',
        'license',
        'help',
    }, vars(__builtins__).keys()

else:  # This file was imported as a module.
    print('not main')

    assert dir() == [
        '__builtins__',
        '__cached__',
        '__doc__',
        '__file__',
        '__loader__',
        '__name__',
        '__package__',
        '__spec__',
    ], dir()

    assert isinstance(__builtins__, dict)
    assert (
        globals().keys() - __builtins__.keys()
        == {'__file__', '__builtins__', '__cached__'}
    ), globals().keys() - __builtins__.keys()

    assert globals().keys() == {
        '__name__',
        '__doc__',
        '__package__',
        '__loader__',
        '__spec__',
        '__file__',
        '__cached__',
        '__builtins__',
    }, globals().keys()

    assert __builtins__.keys() == {
        '__name__',
        '__doc__',
        '__package__',
        '__loader__',
        '__spec__',
        '__build_class__',
        '__import__',
        'abs',
        'all',
        'any',
        'ascii',
        'bin',
        'breakpoint',
        'callable',
        'chr',
        'compile',
        'delattr',
        'dir',
        'divmod',
        'eval',
        'exec',
        'format',
        'getattr',
        'globals',
        'hasattr',
        'hash',
        'hex',
        'id',
        'input',
        'isinstance',
        'issubclass',
        'iter',
        'len',
        'locals',
        'max',
        'min',
        'next',
        'oct',
        'ord',
        'pow',
        'print',
        'repr',
        'round',
        'setattr',
        'sorted',
        'sum',
        'vars',
        'None',
        'Ellipsis',
        'NotImplemented',
        'False',
        'True',
        'bool',
        'memoryview',
        'bytearray',
        'bytes',
        'classmethod',
        'complex',
        'dict',
        'enumerate',
        'filter',
        'float',
        'frozenset',
        'property',
        'int',
        'list',
        'map',
        'object',
        'range',
        'reversed',
        'set',
        'slice',
        'staticmethod',
        'str',
        'super',
        'tuple',
        'type',
        'zip',
        '__debug__',
        'BaseException',
        'Exception',
        'TypeError',
        'StopAsyncIteration',
        'StopIteration',
        'GeneratorExit',
        'SystemExit',
        'KeyboardInterrupt',
        'ImportError',
        'ModuleNotFoundError',
        'OSError',
        'EnvironmentError',
        'IOError',
        'EOFError',
        'RuntimeError',
        'RecursionError',
        'NotImplementedError',
        'NameError',
        'UnboundLocalError',
        'AttributeError',
        'SyntaxError',
        'IndentationError',
        'TabError',
        'LookupError',
        'IndexError',
        'KeyError',
        'ValueError',
        'UnicodeError',
        'UnicodeEncodeError',
        'UnicodeDecodeError',
        'UnicodeTranslateError',
        'AssertionError',
        'ArithmeticError',
        'FloatingPointError',
        'OverflowError',
        'ZeroDivisionError',
        'SystemError',
        'ReferenceError',
        'MemoryError',
        'BufferError',
        'Warning',
        'UserWarning',
        'DeprecationWarning',
        'PendingDeprecationWarning',
        'SyntaxWarning',
        'RuntimeWarning',
        'FutureWarning',
        'ImportWarning',
        'UnicodeWarning',
        'BytesWarning',
        'ResourceWarning',
        'ConnectionError',
        'BlockingIOError',
        'BrokenPipeError',
        'ChildProcessError',
        'ConnectionAbortedError',
        'ConnectionRefusedError',
        'ConnectionResetError',
        'FileExistsError',
        'FileNotFoundError',
        'IsADirectoryError',
        'NotADirectoryError',
        'InterruptedError',
        'PermissionError',
        'ProcessLookupError',
        'TimeoutError',
        'open',
        'quit',
        'exit',
        'copyright',
        'credits',
        'license',
        'help',
    }, __builtins__.keys()


# pp(globals().keys())

# pp(__builtins__.keys())

# dict_keys(['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__', '__builtins__', 'pp'])
# dict_keys(['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__build_class__', '__import__', 'abs', 'all', 'any', 'ascii', 'bin', 'breakpoint', 'callable', 'chr', 'compile', 'delattr', 'dir', 'divmod', 'eval', 'exec', 'format', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'locals', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print', 'repr', 'round', 'setattr', 'sorted', 'sum', 'vars', 'None', 'Ellipsis', 'NotImplemented', 'False', 'True', 'bool', 'memoryview', 'bytearray', 'bytes', 'classmethod', 'complex', 'dict', 'enumerate', 'filter', 'float', 'frozenset', 'property', 'int', 'list', 'map', 'object', 'range', 'reversed', 'set', 'slice', 'staticmethod', 'str', 'super', 'tuple', 'type', 'zip', '__debug__', 'BaseException', 'Exception', 'TypeError', 'StopAsyncIteration', 'StopIteration', 'GeneratorExit', 'SystemExit', 'KeyboardInterrupt', 'ImportError', 'ModuleNotFoundError', 'OSError', 'EnvironmentError', 'IOError', 'EOFError', 'RuntimeError', 'RecursionError', 'NotImplementedError', 'NameError', 'UnboundLocalError', 'AttributeError', 'SyntaxError', 'IndentationError', 'TabError', 'LookupError', 'IndexError', 'KeyError', 'ValueError', 'UnicodeError', 'UnicodeEncodeError', 'UnicodeDecodeError', 'UnicodeTranslateError', 'AssertionError', 'ArithmeticError', 'FloatingPointError', 'OverflowError', 'ZeroDivisionError', 'SystemError', 'ReferenceError', 'MemoryError', 'BufferError', 'Warning', 'UserWarning', 'DeprecationWarning', 'PendingDeprecationWarning', 'SyntaxWarning', 'RuntimeWarning', 'FutureWarning', 'ImportWarning', 'UnicodeWarning', 'BytesWarning', 'ResourceWarning', 'ConnectionError', 'BlockingIOError', 'BrokenPipeError', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionRefusedError', 'ConnectionResetError', 'FileExistsError', 'FileNotFoundError', 'IsADirectoryError', 'NotADirectoryError', 'InterruptedError', 'PermissionError', 'ProcessLookupError', 'TimeoutError', 'open', 'quit', 'exit', 'copyright', 'credits', 'license', 'help'])
# Traceback (most recent call last):

import builtins  # noqa

if __name__ == '__main__':
    print('main')
    assert __builtins__ is builtins
else:
    print('not main')
    print(type(__builtins__))
    assert __builtins__ is globals()

print('*'*80)
raise Exception('done')
