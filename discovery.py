class IndexerError(Exception):
    pass


class NoResults(IndexerError):
    def __init__(self, tags):
        super().__init__(f"No results found with tags {set(tags)}")


class MultipleResults(IndexerError):
    def __init__(self, tags, results):
        msg = f"Multiple results found with tags {set(tags)}:"
        for result in results:
            msg += (f"\n  - {result}")
        super().__init__(msg)


class Indexer:

    def __init__(self):
        self._names = {}
        self._tags = {}

    def add(self, obj, name, tags):
        if name in self._names:
            # TODO: allow subsequent tag additions to the same object?
            raise ValueError(name)

        self._names[name] = obj

        self._tags.setdefault(name, set()).add(name)
        for tag in tags:
            self._tags.setdefault(tag, set()).add(name)

    def filter(self, tags):
        results = set(self._names)
        for tag in tags:
            results &= self._tags[tag]
        return results

    def get(self, tags, *, results=None):
        if results is None:
            results = self.filter(tags)

        if len(results) == 1:
            return self._names[results.pop()]

        if not results:
            raise NoResults(tags)

        raise MultipleResults(tags, results)


class Discoverer:

    def __init__(self, indexer, tags=frozenset()):
        self._indexer = indexer
        self._tags = tags
        self._matches = matches = indexer.filter(tags)

        try:
            self._result = indexer.get(tags, results=matches)
        except IndexerError as exc:
            self._result = None
            self._error = exc
        else:
            self._error = None

    def __getattr__(self, name):
        return type(self)(
            indexer=self._indexer,
            tags=self._tags | {name},
        )

    def __dir__(self):
        return frozenset(self._indexer._tags) - self._tags

    def __call__(self):
        if self._error is None:
            return self._result
        else:
            raise self._error

    def __repr__(self):
        if self._error is None:
            return f"Use () to retrieve {self._result!r}"
        else:
            return str(self._error)
