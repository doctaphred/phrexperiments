from collections import defaultdict


class DiscoveryError(LookupError):
    pass


class NoResults(DiscoveryError):
    def __init__(self, tags):
        super().__init__(f"No objects tagged with {set(tags)}")


class MultipleResults(DiscoveryError):
    def __init__(self, tags, objects):
        msg = f"Multiple objects tagged with {set(tags)}:"
        for obj in objects:
            msg += f"\n  - {obj}"
        super().__init__(msg)


class Indexer:

    def __init__(self):
        self._obj_index = defaultdict(set)
        self._tag_index = defaultdict(set)

    def index(self, obj, tags):
        obj_tags = self._obj_index[obj]

        for tag in tags:
            obj_tags.add(tag)
            self._tag_index[tag].add(obj)

        try:
            name = obj.__name__
        except AttributeError:
            pass
        else:
            obj_tags.add(name)
            self._tag_index[name].add(obj)

    def filter(self, tags):
        objects = set(self._obj_index)
        for tag in tags:
            objects &= self._tag_index[tag]
        return objects

    def filter2(self, tags):
        return {
            obj for obj, obj_tags in self._obj_index.items()
            if obj_tags >= tags
        }


class Discoverer:

    def __init__(self, indexer, tags=frozenset()):
        self._indexer = indexer
        self._tags = tags

    def __getattr__(self, name):
        return type(self)(
            indexer=self._indexer,
            tags=self._tags | {name},
        )

    def __dir__(self):
        return self._indexer._tag_index.keys() - self._tags

    def __call__(self):
        objects = self._indexer.filter(self._tags)
        if not objects:
            raise NoResults(self._tags)
        elif len(objects) == 1:
            return next(iter(objects))
        else:
            raise MultipleResults(self._tags, objects)

    def __repr__(self):
        try:
            obj = self()
        except DiscoveryError as exc:
            return str(exc)
        else:
            return f"Use () to retrieve {obj!r}"


if __name__ == '__main__':
    import numpy as np

    ufuncs_indexer = Indexer()
    ufuncs = Discoverer(ufuncs_indexer)

    # https://docs.scipy.org/doc/numpy/reference/ufuncs.html#available-ufuncs
    ufunc_tags = {
        # Math operations
        'add': {'math', 'binary'},
        'subtract': {'math', 'binary'},
        'multiply': {'math', 'binary'},
        'divide': {'math', 'binary'},
        'logaddexp': {'math', 'binary'},
        'logaddexp2': {'math', 'binary'},
        'true_divide': {'math', 'binary'},
        'floor_divide': {'math', 'binary'},
        'negative': {'math', 'binary'},
        'positive': {'math', 'binary'},
        'power': {'math', 'binary'},
        'remainder': {'math', 'binary'},
        'mod': {'math', 'binary'},
        'fmod': {'math', 'binary', 'floating'},
        'divmod': {'math', 'binary'},
        'absolute': {'math', 'unary'},
        'fabs': {'math', 'unary', 'floating'},
        'rint': {'math', 'unary'},
        'sign': {'math', 'unary'},
        'heaviside': {'math', 'binary'},
        'conj': {'math', 'unary'},
        'exp': {'math', 'unary'},
        'exp2': {'math', 'unary'},
        'log': {'math', 'unary'},
        'log2': {'math', 'unary'},
        'log10': {'math', 'unary'},
        'expm1': {'math', 'unary'},
        'log1p': {'math', 'unary'},
        'sqrt': {'math', 'unary'},
        'square': {'math', 'unary'},
        'cbrt': {'math', 'unary'},
        'reciprocal': {'math', 'unary'},
        'gcd': {'math', 'binary'},
        'lcm': {'math', 'binary'},

        # Trigonometric functions
        'sin': {'trig', 'unary'},
        'cos': {'trig', 'unary'},
        'tan': {'trig', 'unary'},
        'arcsin': {'trig', 'unary', 'inverse'},
        'arccos': {'trig', 'unary', 'inverse'},
        'arctan': {'trig', 'unary', 'inverse'},
        'arctan2': {'trig', 'binary', 'inverse'},
        'hypot': {'trig', 'binary'},
        'sinh': {'trig', 'unary', 'hyperbolic'},
        'cosh': {'trig', 'unary', 'hyperbolic'},
        'tanh': {'trig', 'unary', 'hyperbolic'},
        'arcsinh': {'trig', 'unary', 'inverse', 'hyperbolic'},
        'arccosh': {'trig', 'unary', 'inverse', 'hyperbolic'},
        'arctanh': {'trig', 'unary', 'inverse', 'hyperbolic'},
        'deg2rad': {'trig', 'unary'},
        'rad2deg': {'trig', 'unary'},

        # Bit-twiddling functions
        'bitwise_and': {'bitwise', 'binary'},
        'bitwise_or': {'bitwise', 'binary'},
        'bitwise_xor': {'bitwise', 'binary'},
        'invert': {'bitwise', 'unary'},
        'left_shift': {'bitwise', 'binary'},
        'right_shift': {'bitwise', 'binary'},

        # Comparison functions
        'greater': {'comparison', 'binary'},
        'greater_equal': {'comparison', 'binary'},
        'less': {'comparison', 'binary'},
        'less_equal': {'comparison', 'binary'},
        'not_equal': {'comparison', 'binary'},
        'equal': {'comparison', 'binary'},
        'logical_and': {'comparison', 'binary'},
        'logical_or': {'comparison', 'binary'},
        'logical_xor': {'comparison', 'binary'},
        'logical_not': {'comparison', 'unary'},
        'maximum': {'comparison', 'binary'},
        'minimum': {'comparison', 'binary'},
        'fmax': {'comparison', 'binary', 'floating'},
        'fmin': {'comparison', 'binary', 'floating'},

        # Floating functions
        'isfinite': {'floating', 'unary'},
        'isinf': {'floating', 'unary'},
        'isnan': {'floating', 'unary'},
        'isnat': {'floating', 'unary'},
        # 'fabs': {'floating', 'unary'},  # Duplicated in 'Math operations'
        'signbit': {'floating', 'unary'},
        'copysign': {'floating', 'binary'},
        'nextafter': {'floating', 'binary'},
        'spacing': {'floating', 'unary'},
        'modf': {'floating', 'unary'},
        'ldexp': {'floating', 'binary'},
        'frexp': {'floating', 'unary'},
        # 'fmod': {'floating', 'binary'},  # Duplicated in 'Math operations'
        'floor': {'floating', 'unary'},
        'ceil': {'floating', 'unary'},
        'trunc': {'floating', 'unary'},
    }

    for name, tags in ufunc_tags.items():
        ufuncs_indexer.index(getattr(np, name), tags=tags)

    assert ufuncs.bitwise.unary() is np.invert
    assert ufuncs.unary.bitwise() is np.invert
    assert ufuncs.invert() is np.invert

    assert ufuncs.math.floating.binary() is np.fmod
    assert ufuncs.math.binary.floating() is np.fmod
    assert ufuncs.floating.math.binary() is np.fmod
    assert ufuncs.binary.math.floating() is np.fmod
    assert ufuncs.floating.binary.math() is np.fmod
    assert ufuncs.binary.floating.math() is np.fmod
    assert ufuncs.fmod() is np.fmod

    extra_attrs = dir(ufuncs) - ufunc_tags.keys()
    missing_funcs = ufunc_tags.keys() - dir(ufuncs)

    assert extra_attrs == {
        'binary',
        'bitwise',
        'comparison',
        'conjugate',  # True name of conj
        'floating',
        'hyperbolic',
        'inverse',
        'math',
        'trig',
        'unary',
    }, extra_attrs

    # TODO: Handle aliases better
    assert missing_funcs == {
        'conj',  # alias of 'conjugate'
        'divide',  # alias of 'true_divide'
        'mod',  # alias of 'remainder'
    }, missing_funcs

    # for name in dir(np):
    #     obj = getattr(np, name)
    #     if isinstance(obj, np.ufunc) and name != obj.__name__:
    #         print(name, obj)

    # Prints:
    #     abs <ufunc 'absolute'>
    #     bitwise_not <ufunc 'invert'>
    #     conj <ufunc 'conjugate'>
    #     divide <ufunc 'true_divide'>
    #     mod <ufunc 'remainder'>
