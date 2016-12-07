def build_cmd(*words, flags=(), opts=(), args=(),
              wordf='{}', flagf='-{}', optf='--{}', argf='--{}={}', **kwargs):
    """Parse the args into a single list."""
    result = []
    result.extend(wordf.format(word) for word in words)
    result.extend(flagf.format(flag) for flag in flags)
    result.extend(optf.format(opt) for opt in opts)
    result.extend(argf.format(k, v) for k, v in args)
    result.extend(argf.format(k.replace('_', '-'), kwargs[k]) for k in kwargs)
    return result


class CmdBuilder:

    def __init__(self, *additions, cmd=(), **attrs):
        self.cmd = cmd + additions
        for name in attrs:
            setattr(self, name, attrs[name])

    def __getattribute__(self, name):
        if name.startswith('__') and name.endswith('__'):
            return super().__getattribute__(name)
        return self.__class__(name.replace('_', '-'), **self.__dict__)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.__class__(*key)
        else:
            return self.__class__(key)

    def __call__(self, *args, **kwargs):
        new_attrs = {name: kwargs.pop(name)
                     for name in self.__dict__
                     if name in kwargs}
        additions = build_cmd(*args, **kwargs)
        attrs = {**self.__dict__, **new_attrs}
        return self.__class__(*additions, **attrs)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, ', '.join(
            '{}={}'.format(k, v) for k, v in sorted(self.__dict__.items())))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))
