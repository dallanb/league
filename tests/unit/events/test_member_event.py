import pytest

from src import services, events


def test_member_member_active_sync(reset_db, pause_notification, seed_league, seed_member):
    """
    GIVEN 1 league instance and 1 member instance in the database
    WHEN directly calling event member handle_event member_active
    THEN event member handle_event member_active updates 1 member instance in the database
    """
    key = 'member_active'
    value = {
        'uuid': str(pytest.member_uuid),
        'user_uuid': str(pytest.user_uuid),
        'league_uuid': str(pytest.league.uuid),
        'email': pytest.email
    }
    events.Member().handle_event(key=key, data=value)

    members = services.MemberService().find()

    assert members.total == 1
    assert members.items[0].user_uuid == pytest.user_uuid


def test_member_display_name_updated_sync(reset_db, pause_notification, seed_league, seed_member,
                                          seed_member_materialized):
    """
    GIVEN 1 league instance, 1 member instance and 1 member materialized instance in the database
    WHEN directly calling event member handle_event display_name_updated
    THEN event member handle_event display_name_updated updates 1 member_materialized instance in the database
    """
    key = 'display_name_updated'
    value = {
        'uuid': str(pytest.member_uuid),
        'display_name': 'Oogly Boogly',
    }
    events.Member().handle_event(key=key, data=value)

    members = services.MemberMaterializedService().find()

    assert members.total == 1
    assert members.items[0].display_name == 'Oogly Boogly'


def test_member_avatar_created_sync(reset_db, pause_notification, seed_league, seed_member,
                                    seed_member_materialized):
    """
    GIVEN 1 league instance, 1 member instance and 1 member materialized instance in the database
    WHEN directly calling event member handle_event avatar_created
    THEN event member handle_event avatar_created updates 1 member_materialized instance in the database
    """
    key = 'avatar_created'
    value = {
        'member_uuid': str(pytest.member_uuid),
        's3_filename': '123.jpg',
    }
    events.Member().handle_event(key=key, data=value)

    members = services.MemberMaterializedService().find()

    assert members.total == 1
    assert members.items[0].avatar == '123.jpg'
