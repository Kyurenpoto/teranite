class RawDatetime(str):
    def expired(self) -> bool:
        return True


class FakeRawDatetime(RawDatetime):
    def expired(self) -> bool:
        return str(self) == ""
