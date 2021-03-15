import pytest

from src import services


@pytest.fixture(scope="function")
def seed_member():
    pytest.member = services.MemberService().create(status='pending', user_uuid=pytest.user_uuid,
                                                    email=pytest.email, league=pytest.league)
