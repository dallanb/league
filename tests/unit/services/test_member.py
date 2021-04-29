import pytest
import logging

from src import services, ManualException
from tests.helpers import generate_uuid

member_service = services.MemberService()


###########
# Find
###########
def test_member_find(reset_db, pause_notification, seed_league, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called
    THEN it should return 1 member
    """

    members = member_service.find()
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.uuid == pytest.member.uuid


def test_member_find_by_uuid():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 member
    """
    member = pytest.member
    uuid = member.uuid

    members = member_service.find(uuid=uuid)
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.uuid == uuid


def test_member_find_by_user_uuid():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with user_uuid
    THEN it should return 1 member
    """
    member = pytest.member
    user_uuid = member.user_uuid

    members = member_service.find(user_uuid=user_uuid)
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.user_uuid == user_uuid


def test_member_find_by_league_uuid():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with league_uuid
    THEN it should return 1 member
    """
    member = pytest.member
    league_uuid = member.league_uuid

    members = member_service.find(league_uuid=league_uuid)
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.league_uuid == league_uuid


def test_member_find_expand_league():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with expand argument to also return league
    THEN it should return 1 member
    """
    members = member_service.find(expand=['league'])
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.league.uuid is not None


def test_member_find_w_pagination(pause_notification):
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of members defined in the pagination arguments
    """
    _ = member_service.create(email='dallanbhatti@gmail.com', user_uuid=generate_uuid(), status='invited',
                              league=pytest.league)
    members_0 = member_service.find(page=1, per_page=1)
    assert members_0.total == 2
    assert len(members_0.items) == 1

    members_1 = member_service.find(page=2, per_page=1)
    assert members_1.total == 2
    assert len(members_1.items) == 1
    assert members_1.items[0] != members_0.items[0]

    members = member_service.find(page=1, per_page=2)
    assert members.total == 2
    assert len(members.items) == 2


def test_member_find_w_bad_pagination():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 member
    """
    members = member_service.find(page=3, per_page=3)
    assert members.total == 2
    assert len(members.items) == 0


def test_member_find_by_user_uuid_none_found():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with a random user_uuid
    THEN it should return the 0 member
    """
    members = member_service.find(user_uuid=generate_uuid())
    assert members.total == 0
    assert len(members.items) == 0


def test_member_find_by_non_existent_column():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 member and ManualException with code 400
    """
    try:
        _ = member_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_member_find_by_non_existent_include():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 member and ManualException with code 400
    """
    try:
        _ = member_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_member_find_by_non_existent_expand():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 member and ManualException with code 400
    """
    try:
        _ = member_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_member_create(reset_db, pause_notification, seed_league, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the create method is called
    THEN it should return 1 member and add 1 member instance into the database
    """
    user_uuid = generate_uuid()
    member = member_service.create(status='invited', email='dallanbhatti@gmail.com', user_uuid=user_uuid,
                                   league=pytest.league)

    assert member.uuid is not None
    assert member.user_uuid == user_uuid


def test_member_create_dup_email(pause_notification):
    """
    GIVEN 2 member instance in the database
    WHEN the create method is called with the same email of an existing member
    THEN it should return 0 member and add 0 member instance into the database and ManualException with code 500
    """
    try:
        user_uuid = generate_uuid()
        _ = member_service.create(status='invited', email=pytest.email, user_uuid=user_uuid,
                                  league=pytest.league)
    except ManualException as ex:
        assert ex.code == 500


def test_member_create_dup_user_uuid(pause_notification):
    """
    GIVEN 2 member instance in the database
    WHEN the create method is called with the same user_uuid of an existing member
    THEN it should return 0 member and add 0 member instance into the database and ManualException with code 500
    """
    try:
        _ = member_service.create(status='invited', email='dallanbhatti+0@gmail.com', user_uuid=pytest.user_uuid,
                                  league=pytest.league)
    except ManualException as ex:
        assert ex.code == 500


def test_member_create_w_bad_field(pause_notification):
    """
    GIVEN 2 member instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 member and add 0 member instance into the database and ManualException with code 500
    """
    try:
        _ = member_service.create(status='pending', email='test@sfu.ca', user_uuid=generate_uuid(),
                                  league=pytest.league, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_member_update(reset_db, pause_notification, seed_league, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the update method is called
    THEN it should return 1 member and update 1 member instance into the database
    """
    member = member_service.update(uuid=pytest.member.uuid, status='pending')
    assert member.uuid is not None

    members = member_service.find(uuid=member.uuid)
    assert members.total == 1
    assert len(members.items) == 1
    assert members.items[0].status.name == 'pending'


def test_member_update_w_bad_uuid(reset_db, pause_notification, seed_league, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 member and update 0 member instance into the database and ManualException with code 404
    """
    try:
        _ = member_service.update(uuid=generate_uuid(), status='active')
    except ManualException as ex:
        assert ex.code == 404


def test_member_update_w_bad_field(pause_notification):
    """
    GIVEN 1 member instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 member and update 0 member instance in the database and ManualException with code 400
    """
    try:
        _ = member_service.update(uuid=pytest.member.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_member_apply(reset_db, pause_notification, seed_league, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the apply method is called
    THEN it should return 1 member and update 1 member instance in the database
    """
    member = member_service.apply(instance=pytest.member, status='pending')
    assert member.uuid is not None

    members = member_service.find(uuid=member.uuid)
    assert members.total == 1
    assert len(members.items) == 1


def test_member_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 member instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 member and update 0 member instance in the database and ManualException with code 400
    """
    try:
        _ = member_service.apply(instance=pytest.member, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########
def test_fetch_members(reset_db, mock_fetch_members, seed_league):
    """
    GIVEN 0 member members in the database
    WHEN the create_member method is called
    THEN it should return 1 member
    """
    members = member_service.fetch_members(params={'email': pytest.email, 'league_uuid': str(pytest.league.uuid)})
    member = members[0]
    assert member['uuid'] is not None
    assert member['user_uuid'] == str(pytest.user_uuid)


def test_fetch_member(mock_fetch_member):
    """
    GIVEN 0 member members in the database
    WHEN the create_member method is called
    THEN it should return 1 member
    """
    member = member_service.fetch_member(user_uuid=str(pytest.user_uuid), league_uuid=str(pytest.league.uuid))
    assert member['uuid'] is not None
    assert member['user_uuid'] == str(pytest.user_uuid)


def test_get_member_cache_key(reset_db, reset_cache, seed_league):
    """
    GIVEN 0 member in the cache
    WHEN the get_member_cache_key method is called
    THEN it should return 1 cache_key
    """
    cache_key = member_service.get_member_cache_key(user_uuid=str(pytest.user_uuid),
                                                    league_uuid=str(pytest.league.uuid))
    assert cache_key == f'{str(pytest.user_uuid)}_{str(pytest.league.uuid)}'
    cache_key = member_service.get_member_cache_key(user_uuid=str(pytest.user_uuid))
    assert cache_key == f'{str(pytest.user_uuid)}'


def test_set_member_cache(reset_db, reset_cache, seed_league):
    """
    GIVEN 0 member in the cache
    WHEN the set_member_cache method is called
    THEN it should return true
    """
    cache_key = member_service.get_member_cache_key(user_uuid=str(pytest.user_uuid),
                                                    league_uuid=str(pytest.league.uuid))
    res = member_service.set_member_cache(key=cache_key, val={'ping': 'pong'}, timeout=3600)
    assert res is True


def test_get_member_cache(reset_db, reset_cache, seed_league):
    """
    GIVEN 1 member in the cache
    WHEN the get_member_cache method is called
    THEN it should return 1 member
    """
    cache_key = member_service.get_member_cache_key(user_uuid=str(pytest.user_uuid),
                                                    league_uuid=str(pytest.league.uuid))
    val = {'ping': 'pong'}
    _ = member_service.set_member_cache(key=cache_key, val=val, timeout=3600)
    member = member_service.get_member_cache(key=cache_key)
    assert member == val


def test_delete_member_cache(reset_db, reset_cache, seed_league):
    """
    GIVEN 1 member in the cache
    WHEN the delete_member_cache method is called
    THEN it should return 1
    """
    cache_key = member_service.get_member_cache_key(user_uuid=str(pytest.user_uuid),
                                                    league_uuid=str(pytest.league.uuid))
    val = {'ping': 'pong'}
    _ = member_service.set_member_cache(key=cache_key, val=val, timeout=3600)
    res = member_service.delete_member_cache(key=cache_key)
    assert res == 1
    member = member_service.get_member_cache(key=cache_key)
    assert member is None
