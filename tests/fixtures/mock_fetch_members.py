import pytest

from tests.helpers import fetch_members


@pytest.fixture
def mock_fetch_members(mocker):
    yield mocker.patch('src.services.MemberService.fetch_members', fetch_members)
