import pytest

from src import services


@pytest.fixture(scope="function")
def seed_avatar():
    s3_filename = services.AvatarService().generate_s3_filename(league_uuid=str(pytest.league.uuid))
    pytest.avatar = services.AvatarService().create(s3_filename=s3_filename)
    services.LeagueService().apply(instance=pytest.league, avatar=pytest.avatar)
