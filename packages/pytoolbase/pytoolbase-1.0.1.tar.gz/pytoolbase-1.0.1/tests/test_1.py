#!/usr/bin/env python3

import logging
import pytest
import warnings
from pytoolbase.retry import retry

warnings.filterwarnings("ignore")
logger = logging.getLogger('tests.test_1')
logger.addHandler(logging.NullHandler())


class TestException(Exception):
    pass


@retry(retry_count=5)
def f_error():
    raise TestException("test exception")


@retry(retry_count=5)
def f_success():
    return 10


@retry(retry_count=5)
async def f_error_a():
    raise TestException("test exception")


@retry(retry_count=5)
async def f_success_a():
    return 10


@pytest.mark.serial
class TestRetry(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_1(self):
        try:
            result = f_error()
            logger.debug(f"test_1 result: {result}")
        except TestException:
            pass
        assert f_error.calls == 5

    def test_2(self):
        try:
            result = f_success()
            logger.debug(f"test_2 result: {result}")
            assert result == 10
        except TestException:
            pass
        assert f_success.calls == 0

    @pytest.mark.asyncio
    async def test_3(self):
        try:
            result = await f_error_a()
            logger.debug(f"test_3 result: {result}")
        except TestException:
            pass
        assert f_error_a.calls == 5

    @pytest.mark.asyncio
    async def test_4(self):
        try:
            result = await f_success_a()
            logger.debug(f"test_4 result: {result}")
            assert result == 10
        except TestException:
            pass
        assert f_success_a.calls == 0
