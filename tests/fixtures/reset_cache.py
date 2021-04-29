import pytest

from src import common


@pytest.fixture(scope='function')
def reset_cache():
    cache = common.Cache()
    cache.clear()
