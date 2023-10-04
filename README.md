# Versatile ContextDecorator
A ContextDecorator base for making decorators/contextmanagers that will work with both async and non-async code


## Why do I need this?
Reusing code is considered good practice. With that in mind, when writing something like a timer log decorator, one might find himself in an odd situation. ContextDecorator in python's standard library cannot run with `async with` and it won't be able to run async functions. Of course we can use AsyncContextDecorator and have two classes for different scenarios, but why not have one?

There is a bit of [relevant discussion](https://github.com/python/cpython/issues/81579) as to why this is not standard library. Feedback from this discussion was used to make this library more reliable. If there is a need to specify how a decorated function should be handled, it was added to the implementation. 


## Example
Best examples, as often is the case, will be found in tests. Here is one, along with some small use examples:
``` python
from time import perf_counter

from versatile_context_decorator import ContextDecorator


class timer_log(ContextDecorator):
    """A useful example defined based on the versatile ContextDecorator"""

    def __init__(self, logger: Logger, is_async: bool | None = None, label: str | None = None):
        self.logger = logger
        self.label = label
        super().__init__(is_async)

    def __call__(self, func):
        if not self.label:
            self.label = func.__name__

        return super().__call__(func)

    def __enter__(self):
        self.start_time = perf_counter()

    def __exit__(self, *exc):
        self.logger.info(f"Timed '{self.label}': {round(perf_counter() - self.start_time, 2)}s")
        return False
```

Use the class you created like this:
```python
@timer_log(log)
def some_function(...):
    ...

@timer_log(log)
async def some_other_function(...):
    ...

with timer_log(log, label="request to <...> service"):
    ...

async with ClientSession() as session, timer_log(log, label="request to <...> service"):
    ...
```