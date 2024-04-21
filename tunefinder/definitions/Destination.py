from types import SimpleNamespace


class Destination:
    def __init__(self, id: str = None, resolver: SimpleNamespace = None):
        self.id = id
        self.resolver = resolver
