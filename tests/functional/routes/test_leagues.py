import json

import pytest

###########
# Fetch
###########
from src import app, services


#############
# SUCCESS
#############

###########
# Fetch
###########
def test_fetch_league(reset_db, pause_notification, seed_league, seed_member, seed_member_materialized):
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
    assert leagues['status'] == 'active'
    assert leagues['uuid'] == str(league_uuid)
    assert leagues['owner_uuid'] == str(pytest.user_uuid)
    assert leagues['name'] == pytest.league_name


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

    # Request
    response = app.test_client().get(f'/leagues', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['leagues']) == 1
    leagues = response['data']['leagues'][0]
    assert leagues['status'] == 'active'
    assert leagues['uuid'] == str(pytest.league.uuid)
    assert leagues['owner_uuid'] == str(pytest.user_uuid)
    assert leagues['name'] == pytest.league_name


def test_fetch_all_member_user_league():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member_user_leagues' is requested
    THEN check that the response is valid
    """
    user_uuid = pytest.user_uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'member_status': 'pending'}

    # Request
    response = app.test_client().get(f'/members/leagues/user/{user_uuid}', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['leagues']) == 1
    league = response['data']['leagues'][0]['league']
    member = response['data']['leagues'][0]['member']
    assert league['status'] == 'active'
    assert league['uuid'] == str(pytest.league.uuid)
    assert league['owner_uuid'] == str(pytest.user_uuid)
    assert league['name'] == pytest.league_name
    assert member['user'] == str(pytest.user_uuid)


def test_fetch_all_my_member_user_league():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member_user_leagues' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'member_status': 'pending'}

    # Request
    response = app.test_client().get(f'/members/leagues/user/me', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['leagues']) == 1
    league = response['data']['leagues'][0]['league']
    member = response['data']['leagues'][0]['member']
    assert league['status'] == 'active'
    assert league['uuid'] == str(pytest.league.uuid)
    assert league['owner_uuid'] == str(pytest.user_uuid)
    assert league['name'] == pytest.league_name
    assert member['user'] == str(pytest.user_uuid)


###########
# Create
###########
def test_create_league(reset_db, pause_notification, mock_fetch_member):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'league' is requested
    THEN check that the response is valid
    """
    league_name = pytest.league_name
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'name': league_name}

    # Request
    response = app.test_client().post(f'/leagues', json=payload, headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    leagues = response['data']['leagues']
    assert leagues['uuid'] is not None
    assert leagues['name'] == league_name


###########
# Update
###########
def test_update_league(pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'league' is requested
    THEN check that the response is valid
    """
    league_uuid = services.LeagueService().find().items[0].uuid
    league_name = 'Super Duper League'

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'name': league_name}

    # Request
    response = app.test_client().put(f'/leagues/{league_uuid}', json=payload, headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    leagues = response['data']['leagues']
    assert leagues['uuid'] is not None
    assert leagues['name'] == league_name


#############
# FAIL
#############


###########
# Create
###########
def test_create_league_fail(reset_db, pause_notification, mock_fetch_member):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'league' is requested
    THEN check that the response is valid
    """
    league_name = pytest.league_name
    user_uuid = pytest.user_uuid
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'name': league_name, 'owner_uuid': user_uuid}

    # Request
    response = app.test_client().post(f'/leagues', json=payload, headers=headers)

    # Response
    assert response.status_code == 400


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
