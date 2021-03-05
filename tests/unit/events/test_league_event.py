import pytest

from src import services, events


def test_league_member_pending_sync(reset_db, pause_notification, mock_fetch_member, seed_league, seed_member,
                                    seed_member_materialized):
    """
    GIVEN 1 league instance and 1 member instance in the database
    WHEN directly calling event league handle_event member_pending
    THEN event league handle_event member_pending updates 1 member materialized instance in the database
    """
    key = 'member_pending'
    value = {
        'uuid': str(pytest.member.uuid),
        'user_uuid': str(pytest.user_uuid),
        'league_uuid': str(pytest.league.uuid)  # add the rest of the fields as you need them
    }

    events.League().handle_event(key=key, data=value)

    members = services.MemberMaterializedService().find()

    assert members.total == 1
    assert members.items[0].display_name == pytest.display_name


def test_league_member_active_sync(reset_db, pause_notification, mock_fetch_member, seed_league, seed_member,
                                   seed_member_materialized):
    """
    GIVEN 1 league instance and 1 member instance in the database
    WHEN directly calling event league handle_event member_active
    THEN event league handle_event member_active updates 1 member materialized instance in the database
    """
    key = 'member_active'
    value = {
        'uuid': str(pytest.member.uuid),
        'user_uuid': str(pytest.user_uuid),
        'league_uuid': str(pytest.league.uuid)  # add the rest of the fields as you need them
    }

    events.League().handle_event(key=key, data=value)

    members = services.MemberMaterializedService().find()

    assert members.total == 1
    assert members.items[0].display_name == pytest.display_name


def test_league_member_inactive_sync(reset_db, pause_notification, mock_fetch_member, seed_league, seed_member,
                                     seed_member_materialized):
    """
    GIVEN 1 league instance and 1 member instance in the database
    WHEN directly calling event league handle_event member_inactive
    THEN event league handle_event member_inactive updates 1 member materialized instance in the database
    """
    key = 'member_inactive'
    value = {
        'uuid': str(pytest.member.uuid),
        'user_uuid': str(pytest.user_uuid),
        'league_uuid': str(pytest.league.uuid)  # add the rest of the fields as you need them
    }

    events.League().handle_event(key=key, data=value)

    members = services.MemberMaterializedService().find()

    assert members.total == 1
    assert members.items[0].display_name == pytest.display_name
