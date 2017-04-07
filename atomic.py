from contextlib import contextmanager


@contextmanager
def transaction(*objs):
    """Revert all changes to objs if an exception occurs.

    Example usage:

        original_balance = bank.balance
        with transaction(bank):
            bank.transfer(stocks)
            time.sleep(10000)
            stocks.transfer(bank)
            if bank.balance < original_balance:
                raise DontInvestAfterAll
    """
    originals = [obj.__dict__.copy() for obj in objs]
    try:
        yield
    except Exception:
        for obj, original in zip(objs, originals):
            obj.__dict__ = original
        raise


if __name__ == '__main__':
    def obj(): pass
    obj.attr = 1
    try:
        with transaction(obj):
            obj.attr += 1
            assert obj.attr == 2
            raise TabError
    except Exception:
        pass
    assert obj.attr == 1
