from collections.abc import MutableMapping
from weakref import finalize, WeakKeyDictionary, WeakValueDictionary


class IdentityDict(MutableMapping):
    """A dict keyed off of object IDs -- hashability not required."""

    def __init__(self):
        self._keys = {}
        self._values = {}

    def __getitem__(self, key):
        return self._values[id(key)]

    def __setitem__(self, key, value):
        self._keys[id(key)] = key
        self._values[id(key)] = value

    def __delitem__(self, key):
        del self._keys[id(key)]
        del self._values[id(key)]

    def __iter__(self):
        return iter(self._keys.values())

    def __len__(self):
        return len(self._values)


class WeakKeyIdentityDictionary(IdentityDict):

    def __init__(self):
        self._keys = WeakValueDictionary()
        self._values = {}

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        finalize(key, lambda: self._values.pop(id(key), None))


class WeakValueIdentityDictionary(IdentityDict):

    def __init__(self):
        self._keys = {}
        self._values = WeakKeyDictionary()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        finalize(key, lambda: self._keys.pop(id(key), None))
