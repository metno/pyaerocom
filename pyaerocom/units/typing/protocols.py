from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsMul(Protocol):
    def __mul__(self, other): ...

    def __rmul__(self, other): ...
