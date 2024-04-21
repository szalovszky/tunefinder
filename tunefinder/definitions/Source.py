from types import SimpleNamespace
from tunefinder.definitions.Url import Url


class Source:
    def __init__(self, id: str = None, url: Url = None, resolver: SimpleNamespace = None):
        self.id = id
        self.url = url
        self.resolver = resolver
