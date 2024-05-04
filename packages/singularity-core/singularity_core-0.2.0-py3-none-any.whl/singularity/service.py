from typing import Any, TypeVar

T = TypeVar("T")


class Base:
    """
    Base class for service.
    """

    async def __int__(self, model: T):
        self.model = model

    def list(self, *, skip: int = 0, limit: int = 10) -> Any: ...

    def get(self, id: int) -> Any: ...

    def post(self, data: T) -> Any: ...

    def update(self, data: T) -> Any: ...

    def delete(self, id: int) -> Any: ...
