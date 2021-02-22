from uuid import uuid4

import pytest

from .fixtures import *

def pytest_configure(config):
    pytest.league = None
    pytest.member = None
    pytest.avatar = None
    pytest.user_uuid = uuid4()
    pytest.member_uuid = uuid4()
    pytest.user_uuid = uuid4()
    pytest.league_name = 'Super League'
    pytest.email = 'dallan.bhatti@techtapir.com'
    pytest.display_name = 'Dallan Bhatti'
    pytest.username = 'dallanbhatti'
    pytest.country = 'CA'