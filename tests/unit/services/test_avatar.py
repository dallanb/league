import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

avatar_service = services.AvatarService()


###########
# Find
###########
def test_find_avatar(reset_db, pause_notification, seed_league, seed_avatar):
    """
    GIVEN 1 avatar instance in the database
    WHEN the find method is called
    THEN it should return 1 avatar
    """

    avatars = avatar_service.find()
    assert avatars.total == 1


def test_find_avatar_by_uuid():
    """
    GIVEN 1 avatar instance in the database
    WHEN the find method is called
    THEN it should return 1 avatar
    """

    avatars = avatar_service.find(uuid=pytest.avatar.uuid)
    assert avatars.total == 1


def test_avatar_find_expand_league():
    """
    GIVEN 1 avatar instance in the database
    WHEN the find method is called with uuid and with expand argument to also return league
    THEN it should return 1 avatar
    """

    avatars = avatar_service.find(uuid=pytest.avatar.uuid, expand=['league'])

    assert avatars.total == 1
    assert len(avatars.items) == 1
    avatar = avatars.items[0]
    assert avatar.league is not None
    assert avatar.league.uuid is not None


def test_avatar_find_expand_league():
    """
    GIVEN 1 avatar instance in the database
    WHEN the find method is called with uuid and with expand argument to also return league
    THEN it should return 1 avatar
    """

    avatars = avatar_service.find(uuid=pytest.avatar.uuid, expand=['league'])

    assert avatars.total == 1
    assert len(avatars.items) == 1
    avatar = avatars.items[0]
    assert avatar.league is not None
    assert avatar.league.uuid is not None


def test_avatar_find_w_pagination(pause_notification):
    """
    GIVEN 2 avatar instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of avatars defined in the pagination arguments
    """
    league = services.LeagueService().create(status='active',
                                             name='Test League',
                                             owner_uuid=pytest.user_uuid)
    s3_filename = avatar_service.generate_s3_filename(league_uuid=str(league.uuid))
    avatar = avatar_service.create(s3_filename=s3_filename)
    services.LeagueService().apply(instance=league, avatar=avatar)

    avatars_0 = avatar_service.find(page=1, per_page=1)
    assert avatars_0.total == 2
    assert len(avatars_0.items) == 1

    avatars_1 = avatar_service.find(page=2, per_page=1)
    assert avatars_1.total == 2
    assert len(avatars_1.items) == 1
    assert avatars_1.items[0] != avatars_0.items[0]

    avatars = avatar_service.find(page=1, per_page=2)
    assert avatars.total == 2
    assert len(avatars.items) == 2


def test_avatar_find_w_bad_pagination():
    """
    GIVEN 2 avatar instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 avatar
    """
    avatars = avatar_service.find(page=3, per_page=3)
    assert avatars.total == 2
    assert len(avatars.items) == 0


def test_avatar_find_by_non_existent_column():
    """
    GIVEN 2 avatar instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 avatar and ManualException with code 400
    """
    try:
        _ = avatar_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_avatar_find_by_non_existent_include():
    """
    GIVEN 2 avatar instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 avatar and ManualException with code 400
    """
    try:
        _ = avatar_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_avatar_find_by_non_existent_expand():
    """
    GIVEN 2 avatar instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 avatar and ManualException with code 400
    """
    try:
        _ = avatar_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_avatar_create(reset_db, pause_notification, seed_league):
    """
    GIVEN 0 avatar instance in the database
    WHEN the create method is called
    THEN it should return 1 avatar and add 1 avatar instance into the database
    """
    s3_filename = avatar_service.generate_s3_filename(league_uuid=str(pytest.league.uuid))
    avatar = avatar_service.create(s3_filename=s3_filename, league=pytest.league)

    assert avatar.uuid is not None
    assert avatar.s3_filename == s3_filename


def test_avatar_create_w_bad_field(reset_db, pause_notification, seed_league):
    """
    GIVEN 0 avatar instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 avatar and add 0 avatar instance into the database and ManualException with code 500
    """
    try:
        s3_filename = avatar_service.generate_s3_filename(league_uuid=str(pytest.league.uuid))
        _ = avatar_service.create(s3_filename=s3_filename, league=pytest.league, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Destroy
###########
def test_avatar_destroy(reset_db, pause_notification, seed_league, seed_avatar):
    """
    GIVEN 1 avatar instance in the database
    WHEN the destroy method is called
    THEN it should return True and remove 1 avatar instance in the database
    """
    avatar = avatar_service.destroy(uuid=pytest.avatar.uuid)
    assert avatar

    avatars = avatar_service.find()
    assert avatars.total == 0


def test_avatar_destroy_w_bad_uuid(reset_db, pause_notification, seed_league, seed_avatar):
    """
    GIVEN 1 avatar instance in the database
    WHEN the destroy method is called with random uuid
    THEN it should return ManualException with code 404
    """
    try:
        _ = avatar_service.destroy(uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 404


###########
# Misc
###########
def test_upload_file(reset_db, pause_notification, mock_upload_file):
    """
    GIVEN 0 avatar instance in the database
    WHEN the upload_file method is called
    THEN it should return True and supposedly add a file to AWS S3
    """
    file = avatar_service.upload_file(filename='test.jpg')
    assert file


def test_upload_fileobj(reset_db, pause_notification, mock_upload_fileobj):
    """
    GIVEN 0 avatar instance in the database
    WHEN the upload_fileobj method is called
    THEN it should return True and supposedly add a file to AWS S3
    """
    file = avatar_service.upload_fileobj(file='test', filename='test')
    assert file


def test_generate_s3_filename(reset_db, pause_notification):
    """
    GIVEN 0 avatar instance in the database
    WHEN the generate_s3_filename method is called
    THEN it should return a filename
    """
    uuid = generate_uuid()
    filename = avatar_service.generate_s3_filename(uuid)
    assert filename == f'{uuid}.jpeg'
