import pytest

from tests.helpers import upload_file


@pytest.fixture
def mock_upload_file(mocker):
    yield mocker.patch('src.services.AvatarService.upload_file', upload_file)
