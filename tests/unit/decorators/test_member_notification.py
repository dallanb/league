import pytest

from src import services


def test_member_notification_member_invited(reset_db, kafka_conn_last_msg, mock_league_notification_create,
                                            seed_league):
    pytest.member = services.MemberService().create(status='invited', email=pytest.email, league=pytest.league)
    msg = kafka_conn_last_msg('leagues')
    assert msg.key is not None
    assert msg.key == 'member_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)


def test_member_notification_member_pending(reset_db, mock_league_notification_create, seed_league,
                                            kafka_conn_last_msg):
    pytest.member = services.MemberService().create(status='pending', user_uuid=pytest.user_uuid,
                                                    email=pytest.email, league_uuid=pytest.league.uuid)
    msg = kafka_conn_last_msg('leagues')
    assert msg.key is not None
    assert msg.key == 'member_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)


def test_member_notification_member_active(kafka_conn_last_msg):
    pytest.member = services.MemberService().update(uuid=pytest.member.uuid, status='active')
    msg = kafka_conn_last_msg('leagues')
    assert msg.key is not None
    assert msg.key == 'member_active'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)


def test_member_notification_member_inactive(kafka_conn_last_msg):
    pytest.member = services.MemberService().update(uuid=pytest.member.uuid, status='inactive')
    msg = kafka_conn_last_msg('leagues')
    assert msg.key is not None
    assert msg.key == 'member_inactive'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)
