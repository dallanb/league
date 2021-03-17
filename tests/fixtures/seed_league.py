import pytest

from src import services


@pytest.fixture(scope="function")
def seed_league():
    pytest.league = services.LeagueService().create(status='active', owner_uuid=pytest.user_uuid,
                                                    name=pytest.league_name)
