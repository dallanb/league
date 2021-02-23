import pytest

from src import services
from src.common import DB, Cleaner
from src.models import *
from tests.helpers import generate_uuid

db = DB()
cleaner = Cleaner()


def test_init(reset_db):
    """
    GIVEN a db instance
    WHEN calling the init method of the db instance on the Avatar model
    THEN it should return the avatar instance
    """
    instance = db.init(model=Avatar, s3_filename='test.jpg')
    assert cleaner.is_mapped(instance) == instance
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.s3_filename == 'test.jpg'

    db.rollback()


def test_count():
    """
    GIVEN a db instance
    WHEN calling the count method of the db instance on the Avatar model
    THEN it should return the number of avatar instances
    """
    count = db.count(model=Avatar)
    assert count == 0

    avatar = db.init(model=Avatar, s3_filename='test.jpg')
    _ = db.save(instance=avatar)
    count = db.count(model=Avatar)
    assert count == 1


def test_add(reset_db):
    """
    GIVEN a db instance
    WHEN calling the add method of the db instance on a avatar instance
    THEN it should add a avatar instance to the database
    """
    instance = db.init(model=Avatar, s3_filename='test.jpg')
    avatar = db.add(instance=instance)
    assert cleaner.is_uuid(avatar.uuid) is not None
    assert avatar.s3_filename == 'test.jpg'

    db.rollback()
    assert db.count(model=Avatar) == 0


def test_commit(reset_db):
    """
    GIVEN a db instance
    WHEN calling the commit method of the db instance on a avatar instance
    THEN it should add a avatar instance to the database
    """
    instance = db.init(model=Avatar, s3_filename='test.jpg')
    avatar = db.add(instance=instance)
    assert cleaner.is_uuid(avatar.uuid) is not None
    assert avatar.s3_filename == 'test.jpg'

    db.rollback()
    assert db.count(model=Avatar) == 0

    _ = db.add(instance=instance)
    db.commit()
    assert db.count(model=Avatar) == 1

    instance_0 = db.init(model=Avatar, s3_filename='test.jpg')
    instance_1 = db.init(model=Avatar, s3_filename='test.jpg')
    instance_2 = db.init(model=Avatar, s3_filename='test.jpg')
    db.add(instance=instance_0)
    db.add(instance=instance_1)
    db.add(instance=instance_2)
    db.commit()
    assert db.count(model=Avatar) == 4


def test_save(reset_db):
    """
    GIVEN a db instance
    WHEN calling the save method of the db instance on a avatar instance
    THEN it should add a avatar instance to the database
    """
    instance = db.init(model=Avatar, s3_filename='test.jpg')
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.s3_filename == 'test.jpg'
    avatar = db.save(instance=instance)
    assert db.count(model=Avatar) == 1
    assert avatar.s3_filename == 'test.jpg'


def test_find():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance
    THEN it should find a avatar instance from the database
    """
    result = db.find(model=Avatar)
    assert result.total == 1
    assert len(result.items) == 1

    result = db.find(model=Avatar, uuid=generate_uuid())
    assert result.total == 0


def test_destroy():
    """
    GIVEN a db instance
    WHEN calling the destroy method of the db instance on a avatar instance
    THEN it should remove the avatar instance from the database
    """
    result = db.find(model=Avatar)
    assert result.total == 1
    assert len(result.items) == 1
    instance = result.items[0]

    assert db.destroy(instance=instance)
    assert db.count(model=Avatar) == 0


def test_rollback(reset_db):
    """
    GIVEN a db instance
    WHEN calling the rollback method of the db instance
    THEN it should rollback a avatar instance from being inserted the database
    """
    instance = db.init(model=Avatar, s3_filename='test.jpg')
    db.rollback()
    db.commit()
    assert db.count(model=Avatar) == 0

    instance = db.init(model=Avatar, s3_filename='test.jpg')
    db.save(instance=instance)
    db.rollback()
    assert db.count(model=Avatar) == 1


def test_clean_query(reset_db):
    """
    GIVEN a db instance
    WHEN calling the clean_query method of the db instance
    THEN it should return a query
    """
    query = db.clean_query(model=Avatar)
    assert query is not None


def test_run_query(reset_db, pause_notification, seed_league, seed_avatar):
    """
    GIVEN a db instance
    WHEN calling the run_query method of the db instance with a valid query
    THEN it should return the query result
    """
    query = db.clean_query(model=Avatar)
    avatars = db.run_query(query=query)
    assert avatars.total == 1


def test_equal_filter():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with an equal filter
    THEN it should return the query result
    """
    s3_filename = f'{str(pytest.league.uuid)}.jpeg'
    avatars = db.find(model=Avatar, s3_filename=s3_filename)
    assert avatars.total == 1

    avatars = db.find(model=Avatar, s3_filename=s3_filename, uuid=pytest.avatar.uuid)
    assert avatars.items[0] == pytest.avatar


def test_nested_filter(reset_db, pause_notification, seed_league, seed_avatar):
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with a nested filter
    THEN it should return the query result
    """

    services.LeagueService().apply(instance=pytest.league, avatar=pytest.avatar)

    avatars = db.find(model=Avatar, nested={'league': {'uuid': pytest.league.uuid}})
    assert avatars.total == 1


def test_within_filter():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with a within filter
    THEN it should return the query result
    """

    avatars = db.find(model=Avatar)
    assert avatars.total == 1

    avatars = db.find(model=Avatar, within={'uuid': [pytest.avatar.uuid]})
    assert avatars.total == 1

# def test_has_key_filter():
#     """
#     GIVEN a db instance
#     WHEN calling the find method of the db instance with a has_key filter
#     THEN it should return the query result
#     """
#     
#
#     avatars = db.find(model=Avatar)
#     assert avatars.total == 2
#
#     avatars = db.find(model=Avatar, has_key={'uuid': global_avatar.uuid})
#     assert avatars.total == 0
