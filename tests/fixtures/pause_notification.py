import pytest


@pytest.fixture(scope="function")
def pause_notification(mock_league_notification_create, mock_league_notification_update,
                       mock_member_notification_create, mock_member_notification_update):
    return True
