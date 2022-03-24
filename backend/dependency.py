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


class TypeContainer:
    pass


class InstanceContainer:
    pass


class Provider(NamedTuple):
    types = TypeContainer()
    instances = InstanceContainer()

    def __getitem__(self, name):
        if name not in self.instances.__dict__:
            self.instances.__dict__[name] = self.types.__dict__[name]()

        return self.instances.__dict__[name]

    def wire(self, container: dict):
        self.unwire()

        self.types.__dict__ = container

    def unwire(self):
        self.types.__dict__ = {}
        self.instances.__dict__ = {}


provider = Provider()
