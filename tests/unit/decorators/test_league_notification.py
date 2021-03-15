import time

import pytest

from src import services


def test_league_notification_league_created(reset_db, kafka_conn_last_msg):
    pytest.league = services.LeagueService().create(status='active', name=pytest.league_name,
                                                    owner_uuid=pytest.user_uuid)
    time.sleep(0.5)
    msg = kafka_conn_last_msg('leagues')
    assert msg.key is not None
    assert msg.key == 'league_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.league.uuid)


def test_league_notification_league_inactive(kafka_conn_last_msg):
    _ = services.LeagueService().update(uuid=pytest.league.uuid, status='inactive')
    time.sleep(0.5)
    msg = kafka_conn_last_msg('leagues')
    assert msg.key is not None
    assert msg.key == 'league_inactive'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.league.uuid)


def test_league_notification_name_updated(kafka_conn_last_msg):
    _ = services.LeagueService().update(uuid=pytest.league.uuid, name='Oogly Boogly')
    time.sleep(0.5)
    msg = kafka_conn_last_msg('leagues')
    assert msg.key is not None
    assert msg.key == 'name_updated'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.league.uuid)
    assert msg.value['name'] == 'Oogly Boogly'
