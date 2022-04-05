from typing import Any, NamedTuple


class TypeValue(NamedTuple):
    value: Any

    def __call__(self):
        return self.value


class TypeFactory(NamedTuple):
    typeObject: type
    params: dict

    def __call__(self):
        return self.typeObject(**self.params)


class Provider:
    def __init__(self):
        self.types = [{}]
        self.instances = [{}]

    def __getitem__(self, name):
        if name not in self.instances[0]:
            self.instances[0][name] = self.types[0][name]()

        return self.instances[0][name]

    def wire(self, container: dict):
        self.unwire()

        self.types[0] = container

    def unwire(self):
        self.types[0] = {}
        self.instances[0] = {}


provider = Provider()
