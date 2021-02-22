import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

member_service = services.MemberMaterializedService()


###########
# Find
###########
def test_member_find(reset_db, pause_notification, seed_league, seed_member, seed_member_materialized):
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


def test_member_find_by_league():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with league
    THEN it should return 1 member
    """
    member = pytest.member
    league_uuid = member.league_uuid

    members = member_service.find(league=league_uuid)
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.league == league_uuid


def test_member_find_by_non_existent_column():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 member and ManualException with code 400
    """
    try:
        _ = member_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_member_create(reset_db, pause_notification, seed_league, seed_member, mock_fetch_member):
    """
    GIVEN 0 member instance in the database
    WHEN the create method is called
    THEN it should return 1 member and add 1 member instance into the database
    """
    owner = services.MemberService().fetch_member(user_uuid=str(pytest.user_uuid), league_uuid=str(pytest.league.uuid))
    member = member_service.create(
        uuid=pytest.member.uuid, display_name=owner['display_name'], status='invited',
        email=owner['email'], username=owner['username'],
        member=owner['uuid'], user=owner['user_uuid'], league=pytest.league.uuid, country=pytest.country
    )

    assert member.uuid == pytest.member.uuid


###########
# Update
###########
def test_member_update(reset_db, pause_notification, seed_league, seed_member, seed_member_materialized):
    """
    GIVEN 1 member instance in the database
    WHEN the update method is called
    THEN it should return 1 member and update 1 member instance into the database
    """
    member = member_service.update(uuid=pytest.member.uuid, display_name='Oingo Boingo')
    assert member.uuid is not None

    members = member_service.find(uuid=member.uuid)
    assert members.total == 1
    assert len(members.items) == 1


###########
# Apply
###########
def test_member_apply(reset_db, pause_notification, seed_league, seed_member, seed_member_materialized):
    """
    GIVEN 1 member instance in the database
    WHEN the apply method is called
    THEN it should return 1 member and update 1 member instance in the database
    """
    member = member_service.apply(instance=pytest.member_materialized, display_name='Oingo Boingo')
    assert member.uuid is not None

    members = member_service.find(uuid=member.uuid)
    assert members.total == 1
    assert len(members.items) == 1
