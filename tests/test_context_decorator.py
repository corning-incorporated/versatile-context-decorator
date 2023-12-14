# Copyright (c) 2022-2023 Corning Incorporated. All rights reserved.
# Public - Corning
from logging import INFO, Logger, getLogger
from time import perf_counter

import pytest

from versatile_context_decorator import ContextDecorator

log = getLogger(__name__)


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


def test_decorator(caplog, freezer):
    caplog.set_level(INFO)

    @timer_log(log)
    def some_function():
        freezer.tick(delta=10)  # Make time move 10 seconds

    some_function()

    assert len(caplog.records) == 1
    assert caplog.records[0].msg == "Timed 'some_function': 10.0s"


@pytest.mark.asyncio
async def test_decorator_edgecase(caplog, freezer, mocker):
    """People were worried about iscoroutinefunction being confused. I couldn't get it confused, so
    I am mocking it to be confused and testing the is_async override that way
    """
    caplog.set_level(INFO)
    mocker.patch(
        "versatile_context_decorator.context_decorator.iscoroutinefunction", return_value=True
    )

    @timer_log(log, is_async=False)
    def some_function():
        freezer.tick(delta=10)

    some_function()

    assert len(caplog.records) == 1
    assert caplog.records[0].msg == "Timed 'some_function': 10.0s"


@pytest.mark.asyncio
async def test_async_decorator(caplog, freezer):
    caplog.set_level(INFO)

    @timer_log(log)
    async def some_function():
        freezer.tick(delta=10)

    await some_function()

    assert len(caplog.records) == 1
    assert caplog.records[0].msg == "Timed 'some_function': 10.0s"


def test_context_manager(caplog, freezer):
    caplog.set_level(INFO)

    with timer_log(log, label="my codeblock"):
        freezer.tick(delta=10)

    assert len(caplog.records) == 1
    assert caplog.records[0].msg == "Timed 'my codeblock': 10.0s"


@pytest.mark.asyncio
async def test_async_context_manager(caplog, freezer):
    caplog.set_level(INFO)

    async with timer_log(log, label="my codeblock"):
        freezer.tick(delta=10)

    assert len(caplog.records) == 1
    assert caplog.records[0].msg == "Timed 'my codeblock': 10.0s"
