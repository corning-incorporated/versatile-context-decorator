from contextlib import AsyncContextDecorator
from contextlib import ContextDecorator as SyncContextDecorator
from inspect import iscoroutinefunction

__all__ = ("ContextDecorator",)


class ContextDecorator(AsyncContextDecorator, SyncContextDecorator):
    """A base class or mixin that enables context managers to work as decorators in both async and
    non-async scenarios.

    Params:
    :is_async: when used as decorator, run the function as async or sync depending on the value.
      Otherwise, auto-detection will be used, which can be faulty in rare occasions.
    """

    def __init__(self, is_async: bool | None = None):
        self.is_async = is_async

    def __call__(self, func):
        if iscoroutinefunction(func) if self.is_async is None else self.is_async:
            return AsyncContextDecorator.__call__(self, func)
        else:
            return SyncContextDecorator.__call__(self, func)

    def __enter__(self):
        pass

    def __exit__(self, *exc):
        return False

    # Async context manager support to use in an existing 'async with' if needed
    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, *exc):
        return self.__exit__(*exc)
