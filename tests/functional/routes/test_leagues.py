import json

import pytest

###########
# Fetch
###########
from src import app


#############
# SUCCESS
#############

###########
# Fetch
###########
def test_fetch_league(reset_db, pause_notification, seed_league, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'league' is requested
    THEN check that the response is valid
    """
    league_uuid = pytest.league.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/leagues/{league_uuid}', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    leagues = response['data']['leagues']
    assert leagues['status'] == 'pending'
    assert leagues['uuid'] == str(league_uuid)
    assert leagues['user_uuid'] == str(pytest.user_uuid)
    assert leagues['username'] == pytest.username
    assert leagues['display_name'] == pytest.display_name
    assert leagues['country'] == pytest.country
    assert leagues['league_uuid'] == str(pytest.league_uuid)


def test_fetch_league_user():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'league_user' is requested
    THEN check that the response is valid
    """
    user_uuid = pytest.user_uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid}

    # Request
    response = app.test_client().get(f'/leagues/user/{user_uuid}', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    leagues = response['data']['leagues']
    assert leagues['status'] == 'pending'
    assert leagues['uuid'] == str(pytest.league.uuid)
    assert leagues['user_uuid'] == str(pytest.user_uuid)
    assert leagues['username'] == pytest.username
    assert leagues['display_name'] == pytest.display_name
    assert leagues['country'] == pytest.country
    assert leagues['league_uuid'] == str(pytest.league_uuid)


def test_fetch_my_league_user():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'league_user' is requested
    THEN check that the response is valid
    """
    user_uuid = pytest.user_uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid}

    # Request
    response = app.test_client().get(f'/leagues/user/me', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    leagues = response['data']['leagues']
    assert leagues['status'] == 'pending'
    assert leagues['uuid'] == str(pytest.league.uuid)
    assert leagues['user_uuid'] == str(pytest.user_uuid)
    assert leagues['username'] == pytest.username
    assert leagues['display_name'] == pytest.display_name
    assert leagues['country'] == pytest.country
    assert leagues['league_uuid'] == str(pytest.league_uuid)


###########
# Fetch All
###########
def test_fetch_all_league():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'leagues' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid}

    # Request
    response = app.test_client().get(f'/leagues', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['leagues']) == 1
    leagues = response['data']['leagues'][0]
    assert leagues['status'] == 'pending'
    assert leagues['uuid'] == str(pytest.league.uuid)
    assert leagues['user_uuid'] == str(pytest.user_uuid)
    assert leagues['username'] == pytest.username
    assert leagues['display_name'] == pytest.display_name
    assert leagues['country'] == pytest.country
    assert leagues['league_uuid'] == str(pytest.league_uuid)


def test_fetch_all_league_standings():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'leagues_standings' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid, 'include': 'stat'}

    # Request
    response = app.test_client().get(f'/leagues/standings', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['leagues']) == 1
    leagues = response['data']['leagues'][0]
    assert leagues['status'] == 'pending'
    assert leagues['uuid'] == str(pytest.league.uuid)
    assert leagues['user_uuid'] == str(pytest.user_uuid)
    assert leagues['username'] == pytest.username
    assert leagues['display_name'] == pytest.display_name
    assert leagues['country'] == pytest.country
    assert leagues['league_uuid'] == str(pytest.league_uuid)
    stats = leagues['stat']
    assert stats is not None


def test_fetch_all_league_bulk():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'leagues_bulk' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {
        "within": {
            "key": "uuid",
            "value": [pytest.league.uuid]
        }
    }

    # Request
    response = app.test_client().post(f'/leagues/bulk', headers=headers, json=payload)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['leagues']) == 1
    leagues = response['data']['leagues'][0]
    assert leagues['status'] == 'pending'
    assert leagues['uuid'] == str(pytest.league.uuid)
    assert leagues['user_uuid'] == str(pytest.user_uuid)
    assert leagues['username'] == pytest.username
    assert leagues['display_name'] == pytest.display_name
    assert leagues['country'] == pytest.country
    assert leagues['league_uuid'] == str(pytest.league_uuid)


###########
# Update
###########
def test_update_league(pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'league' is requested
    THEN check that the response is valid
    """
    league_uuid = pytest.league.uuid
    display_name = 'Baby D'

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'display_name': display_name}

    # Request
    response = app.test_client().put(f'/leagues/{league_uuid}', json=payload, headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    leagues = response['data']['leagues']
    assert leagues['uuid'] is not None
    assert leagues['display_name'] == display_name


#############
# FAIL
#############


###########
# Update
###########
def test_update_league_fail(pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'league' is requested
    THEN check that the response is valid
    """
    league_uuid = pytest.league.uuid
    status = 'active'

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'status': status}

    # Request
    response = app.test_client().put(f'/leagues/{league_uuid}', json=payload, headers=headers)

    # Response
    assert response.status_code == 400
