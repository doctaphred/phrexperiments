import time
from subprocess import run
from importlib import import_module


def autoimport(name, attempt, expect=Exception):
    try:
        obj = attempt(name)
    except expect as exc:
        if name.startswith('_'):
            raise
        print(f"Checking globals for {name}...")
        time.sleep(0.5)
        try:
            obj = globals()[name]
        except KeyError:
            print(f"Didn't find it there.")
            print(f"Maybe it's a builtin?")
            time.sleep(1)
            try:
                obj = getattr(__builtins__, name)
            except AttributeError:
                print(f"Nope, not there either. Hmm.")
                print(f"Ah, you probably just forgot to `import {name}`.")
                time.sleep(2)
                try:
                    obj = import_module(name)
                except ModuleNotFoundError:
                    print(f"Hm, don't see nay modules named '{name}'.")
                    print(
                        f"You must have forgotten to install it!"
                        f" Let's fix that..."
                    )
                    time.sleep(4)
                    try:
                        run(['pip', 'install', name], check=True)
                        obj = import_module(name)
                    except Exception:
                        print(f"Aw, that didn't work :( Sorry!")
                        raise exc
                    else:
                        print(f"There you go, now it's installed! :D")

    print(f"Yep! Here you go: {obj}")
    return obj


class ImportingDict(dict):
    def __getitem__(self, key):
        return autoimport(key, super().__getitem__, KeyError)


class DontTryThisAtHome(type):
    def __prepare__(meta, *args, **kwargs):
        return ImportingDict()

    def __getattribute__(self, name):
        return autoimport(name, super().__getattribute__, AttributeError)


if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/doctaphred/emojencode/master/LICENSE'  # noqa

    class packages(metaclass=DontTryThisAtHome):
        print(requests.get(url).text)  # noqa: F821 undefined name

    expected = '😘😗😥😹😈😆😱😭😘😖😼💩'
    result = packages.emojencode.e64encode(b'ayy lmao')
    print(result)
    assert expected == result
