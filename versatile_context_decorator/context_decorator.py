# Copyright (c) 2022-2023 Corning Incorporated. All rights reserved.
# Public - Corning
from abc import ABC, abstractmethod
from contextlib import AsyncContextDecorator
from contextlib import ContextDecorator as SyncContextDecorator
from inspect import iscoroutinefunction

__all__ = ("ContextDecorator",)


class ContextDecorator(AsyncContextDecorator, SyncContextDecorator, ABC):
    """A base class or mixin that enables context managers to work as decorators in both async and
    non-async scenarios.

    Params:
    :is_async: when used as decorator, run the function as async or sync depending on the value.
      Otherwise, auto-detection will be used, which can be faulty in rare occasions.
    """

    def __init__(self, is_async: bool | None = None):
        self.is_async = is_async

    def __call__(self, func):
        _is_async = iscoroutinefunction(func) if self.is_async is None else self.is_async
        if _is_async:
            return AsyncContextDecorator.__call__(self, func)
        else:
            return SyncContextDecorator.__call__(self, func)

    @abstractmethod
    def __enter__(self):
        pass  # pragma: no cover

    @abstractmethod
    def __exit__(self, *exc):
        return False  # pragma: no cover

    # Async context manager support to allow this in an existing 'async with' for brevity
    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, *exc):
        return self.__exit__(*exc)
