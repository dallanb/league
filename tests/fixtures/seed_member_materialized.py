import pytest

from src import services


@pytest.fixture(scope="function")
def seed_member_materialized():
    pytest.member_materialized = services.MemberMaterializedService().create(status='pending', uuid=pytest.member.uuid,
                                                                             display_name=pytest.display_name,
                                                                             email=pytest.email,
                                                                             username=pytest.username,
                                                                             user=pytest.user_uuid,
                                                                             member=pytest.member_uuid,
                                                                             league=pytest.league.uuid,
                                                                             country=pytest.country)
