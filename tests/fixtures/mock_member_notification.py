import pytest

from tests.helpers import member_notification_create, member_notification_update


@pytest.fixture
def mock_member_notification_create(mocker):
    yield mocker.patch('src.decorators.notifications.member_notification.create', member_notification_create)


@pytest.fixture
def mock_member_notification_update(mocker):
    yield mocker.patch('src.decorators.notifications.member_notification.update', member_notification_update)
