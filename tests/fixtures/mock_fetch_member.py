import pytest

from tests.helpers import fetch_member


@pytest.fixture
def mock_fetch_member(mocker):
    yield mocker.patch('src.services.MemberService.fetch_member', fetch_member)
