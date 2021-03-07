import logging
import time

import pytest

from src import services, ManualException
from src.common import time_now
from tests.helpers import generate_uuid

league_service = services.LeagueService()


###########
# Find
###########
def test_league_find(reset_db, pause_notification, seed_league):
    """
    GIVEN 1 league instance in the database
    WHEN the find method is called
    THEN it should return 1 league
    """

    leagues = league_service.find()
    assert leagues.total == 1
    assert len(leagues.items) == 1
    league = leagues.items[0]
    assert league.uuid == pytest.league.uuid


def test_league_find_by_uuid():
    """
    GIVEN 1 league instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 league
    """
    league = pytest.league
    uuid = league.uuid

    leagues = league_service.find(uuid=uuid)
    assert leagues.total == 1
    assert len(leagues.items) == 1
    league = leagues.items[0]
    assert league.uuid == uuid


def test_league_find_by_owner_uuid():
    """
    GIVEN 1 league instance in the database
    WHEN the find method is called with owner_uuid
    THEN it should return 1 league
    """
    league = pytest.league
    owner_uuid = league.owner_uuid

    leagues = league_service.find(owner_uuid=owner_uuid)
    assert leagues.total == 1
    assert len(leagues.items) == 1
    league = leagues.items[0]
    assert league.owner_uuid == owner_uuid


def test_league_find_by_search():
    """
    GIVEN 1 league instance in the database
    WHEN the find method is called with location_uuid
    THEN it should return 1 league
    """
    leagues = league_service.find(search=pytest.league_name[:4])
    assert leagues.total == 1
    assert len(leagues.items) == 1
    league = leagues.items[0]
    assert league.name == pytest.league_name


def test_league_find_include_members(pause_notification, seed_member):
    """
    GIVEN 1 league instance in the database
    WHEN the find method is called with include argument to also return members
    THEN it should return 1 league
    """
    league = pytest.league

    leagues = league_service.find(include=['members'])
    assert leagues.total == 1
    assert len(leagues.items) == 1
    league = leagues.items[0]
    assert len(league.members) == 1


def test_league_find_include_avatar(pause_notification, seed_avatar):
    """
    GIVEN 1 league instance in the database
    WHEN the find method is called with include argument to also return avatar
    THEN it should return 1 league
    """
    leagues = league_service.find(include=['avatar'])
    assert leagues.total == 1
    assert len(leagues.items) == 1
    league = leagues.items[0]
    assert league.avatar is not None


def test_league_find_include_members_include_avatar():
    """
    GIVEN 1 league instance in the database
    WHEN the find method is called with include argument to also return members and avatar
    THEN it should return 1 league
    """
    leagues = league_service.find(include=['members', 'avatar'])
    assert leagues.total == 1
    assert len(leagues.items) == 1
    league = leagues.items[0]
    assert len(league.members) == 1
    assert league.avatar is not None


def test_league_find_w_pagination(pause_notification, seed_league):
    """
    GIVEN 2 league instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of leagues defined in the pagination arguments
    """
    leagues_0 = league_service.find(page=1, per_page=1)
    assert leagues_0.total == 2
    assert len(leagues_0.items) == 1

    leagues_1 = league_service.find(page=2, per_page=1)
    assert leagues_1.total == 2
    assert len(leagues_1.items) == 1
    assert leagues_1.items[0] != leagues_0.items[0]

    leagues = league_service.find(page=1, per_page=2)
    assert leagues.total == 2
    assert len(leagues.items) == 2


def test_league_find_w_bad_pagination():
    """
    GIVEN 2 league instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 league
    """
    leagues = league_service.find(page=3, per_page=3)
    assert leagues.total == 2
    assert len(leagues.items) == 0


def test_league_find_by_owner_uuid_none_found():
    """
    GIVEN 2 league instance in the database
    WHEN the find method is called with a random owner_uuid
    THEN it should return the 0 league
    """
    leagues = league_service.find(owner_uuid=generate_uuid())
    assert leagues.total == 0
    assert len(leagues.items) == 0


def test_league_find_by_non_existent_column():
    """
    GIVEN 2 league instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 league and ManualException with code 400
    """
    try:
        _ = league_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_league_find_by_non_existent_include():
    """
    GIVEN 2 league instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 league and ManualException with code 400
    """
    try:
        _ = league_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_league_find_by_non_existent_expand():
    """
    GIVEN 2 league instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 league and ManualException with code 400
    """
    try:
        _ = league_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_league_create(reset_db, pause_notification):
    """
    GIVEN 0 league instance in the database
    WHEN the create method is called
    THEN it should return 1 league and add 1 league instance into the database
    """
    league = league_service.create(status='active', owner_uuid=pytest.user_uuid, name=pytest.league_name)

    assert league.uuid is not None
    assert league.owner_uuid == pytest.user_uuid


def test_league_create_dup(pause_notification):
    """
    GIVEN 1 league instance in the database
    WHEN the create method is called with the exact same parameters of an existing league
    THEN it should return 1 league and add 1 league instance into the database
    """
    league = league_service.create(status='active', owner_uuid=pytest.user_uuid, name=pytest.league_name)

    assert league.uuid is not None
    assert league.owner_uuid == pytest.user_uuid


def test_league_create_w_bad_field(pause_notification):
    """
    GIVEN 2 league instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 league and add 0 league instance into the database and ManualException with code 500
    """
    try:
        _ = league_service.create(status='pending', owner_uuid=pytest.user_uuid, name=pytest.league_name, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_league_update(reset_db, pause_notification, seed_league):
    """
    GIVEN 1 league instance in the database
    WHEN the update method is called
    THEN it should return 1 league and update 1 league instance into the database
    """
    league = league_service.update(uuid=pytest.league.uuid, name='Oingo Boingo')
    assert league.uuid is not None

    leagues = league_service.find(uuid=league.uuid)
    assert leagues.total == 1
    assert len(leagues.items) == 1


def test_league_update_w_bad_uuid(reset_db, pause_notification, seed_league):
    """
    GIVEN 1 league instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 league and update 0 league instance into the database and ManualException with code 404
    """
    try:
        _ = league_service.update(uuid=generate_uuid(), name='Oingo Boingo')
    except ManualException as ex:
        assert ex.code == 404


def test_league_update_w_bad_field(pause_notification):
    """
    GIVEN 1 league instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 league and update 0 league instance in the database and ManualException with code 400
    """
    try:
        _ = league_service.update(uuid=pytest.league.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_league_apply(reset_db, pause_notification, seed_league):
    """
    GIVEN 1 league instance in the database
    WHEN the apply method is called
    THEN it should return 1 league and update 1 league instance in the database
    """
    league = league_service.apply(instance=pytest.league, name='Oingo Boingo')
    assert league.uuid is not None

    leagues = league_service.find(uuid=league.uuid)
    assert leagues.total == 1
    assert len(leagues.items) == 1


def test_league_apply_w_bad_league(reset_db, pause_notification, seed_league):
    """
    GIVEN 1 league instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 league and update 0 league instance in the database and ManualException with code 404
    """
    try:
        _ = league_service.apply(instance=generate_uuid(), name='Oingo Boingo')
    except ManualException as ex:
        assert ex.code == 400


def test_league_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 league instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 league and update 0 league instance in the database and ManualException with code 400
    """
    try:
        _ = league_service.apply(instance=pytest.league, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########
def test_find_by_participant(reset_db, pause_notification,
                             seed_league, seed_member,
                             seed_member_materialized):
    """
    GIVEN 1 pending league instance, 1 active owner member instance and 1 active member instance in the database
    WHEN the check_league_status method is called
    THEN it should update the league status from 'pending' to 'ready'
    """
    res = league_service.find_by_participant(user_uuid=pytest.user_uuid, user_status='pending', include=[],
                                             paginate={'page': 1, 'per_page': 10})
    assert res.total == 1
    combo = res.items[0]
    assert combo.League is not None
    assert combo.MemberMaterialized is not None
