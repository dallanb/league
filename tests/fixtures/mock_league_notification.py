import pytest

from tests.helpers import league_notification_create, league_notification_update


@pytest.fixture
def mock_league_notification_create(mocker):
    yield mocker.patch('src.decorators.league_notification.create', league_notification_create)


@pytest.fixture
def mock_league_notification_update(mocker):
    yield mocker.patch('src.decorators.league_notification.update', league_notification_update)
