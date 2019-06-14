"""Don't try this at home."""
import time
from subprocess import run
from importlib import import_module


def autoimport(name, otherwise=Exception):
    print(f"Couldn't find {name}. You probably just forgot to import it!")
    time.sleep(2)
    try:
        obj = import_module(name)
    except ModuleNotFoundError:
        print(f"Hm, don't see any modules named '{name}'.")
        print(f"You must have forgotten to install it! Let's fix that...")
        time.sleep(4)
        try:
            run(['pip', 'install', name], check=True)
            obj = import_module(name)
        except Exception:
            print(f"Aw, that didn't work :( Sorry!")
            raise otherwise

    print(f"Found it! Here you go: {obj}")
    return obj


class AutoImportDict(dict):
    def __missing__(self, key):
        if not isinstance(key, str) or key.startswith('_'):
            raise KeyError(key)

        try:
            return globals()[key]
        except KeyError:
            pass

        try:
            return getattr(__builtins__, key)
        except AttributeError:
            pass

        return autoimport(key, KeyError(key))


class AutoImportMeta(type):
    def __prepare__(meta, *args, **kwargs):
        return AutoImportDict()

    def __getattr__(self, name):
        return autoimport(name, AttributeError(name))


class _(metaclass=AutoImportMeta):
    if sys.argv[1:2] != ['--i-understand-the-consequences-of-my-actions']:
        var = os.environ.get('I_UNDERSTAND_THE_CONSEQUENCES_OF_MY_ACTIONS')
        try:
            understood = ast.literal_eval(var)
        except Exception:
            understood = False
        if not understood:
            exit("You don't understand the consequences of your actions.")


if __name__ == '__main__':
    url = (
        'https://'
        'raw.githubusercontent.com'
        '/doctaphred/emojencode/master/LICENSE'
    )

    class packages(metaclass=AutoImportMeta):
        print(requests.get(url).text)

    expected = '😘😗😥😹😈😆😱😭😘😖😼💩'
    result = packages.emojencode.e64encode(b'ayy lmao')
    print(result)
    assert expected == result
