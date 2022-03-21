from typing import NamedTuple


class Container:
    pass


class Provider(NamedTuple):
    container = Container()

    def __getitem__(self, name):
        return self.container.__dict__[name]

    def wire(self, container: dict):
        self.container.__dict__ = container

    def unwire(self):
        self.container.__dict__ = {}


provider = Provider()
