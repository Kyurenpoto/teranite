from typing import NamedTuple


class Provider(NamedTuple):
    container = [{}]

    def dependency(self, name: str):
        return self.container[0][name]

    def wire(self, container: dict):
        self.container[0] = container

    def unwire(self):
        self.container[0] = {}


provider = Provider()
