import pytest

from tests.helpers import upload_fileobj


@pytest.fixture
def mock_upload_fileobj(mocker):
    yield mocker.patch('src.services.AvatarService.upload_fileobj', upload_fileobj)
