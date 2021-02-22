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
def test_fetch_member(reset_db, pause_notification, seed_league, seed_member, seed_member_materialized):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member' is requested
    THEN check that the response is valid
    """
    member_uuid = pytest.member.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/members/{member_uuid}', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['uuid'] == str(member_uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['league_uuid'] == str(pytest.league.uuid)


def test_fetch_member_materialized():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member_materialized' is requested
    THEN check that the response is valid
    """
    member_uuid = pytest.member.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/members/materialized/{member_uuid}', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['uuid'] == str(member_uuid)
    assert members['user'] == str(pytest.user_uuid)
    assert members['league'] == str(pytest.league.uuid)


def test_fetch_member_user_materialized():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member_user_materialized' is requested
    THEN check that the response is valid
    """
    user_uuid = pytest.user_uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league.uuid}

    # Request
    response = app.test_client().get(f'/members/materialized/user/{user_uuid}', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user'] == str(pytest.user_uuid)
    assert members['league'] == str(pytest.league.uuid)


###########
# Fetch All
###########
def test_fetch_all_member():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'members' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/members', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['members']) == 1
    members = response['data']['members'][0]
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['league_uuid'] == str(pytest.league.uuid)


def test_fetch_all_member_materialized():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'members_materialized' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/members/materialized', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['members']) == 1
    members = response['data']['members'][0]
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user'] == str(pytest.user_uuid)
    assert members['league'] == str(pytest.league.uuid)


###########
# Create
###########
def test_create_member(reset_db, pause_notification, mock_fetch_member, mock_fetch_members, seed_league):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'members' is requested
    THEN check that the response is valid
    """
    league_uuid = pytest.league.uuid
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'user_uuid': pytest.user_uuid, 'email': pytest.email}

    # Request
    response = app.test_client().post(f'/leagues/{league_uuid}/members', json=payload, headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['uuid'] is not None
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['league_uuid'] == str(league_uuid)


###########
# Update
###########
def test_update_member(pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'member' is requested
    THEN check that the response is valid
    """
    member_uuid = services.MemberService().find().items[0].uuid
    status = 'active'

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'status': status}

    # Request
    response = app.test_client().put(f'/members/{member_uuid}', json=payload, headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['uuid'] is not None

#############
# FAIL
#############


###########
# Create
###########
def test_create_member_fail(reset_db, pause_notification, mock_fetch_member , mock_fetch_members, seed_league):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'members' is requested
    THEN check that the response is valid
    """
    league_uuid = pytest.league.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'user_uuid': pytest.user_uuid, 'email': pytest.email, 'junk': 'junk'}

    # Request
    response = app.test_client().post(f'/leagues/{league_uuid}/members', json=payload, headers=headers)

    # Response
    assert response.status_code == 400


###########
# Update
###########
def test_update_member_fail(pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'member' is requested
    THEN check that the response is valid
    """
    member_uuid = pytest.member.uuid
    status = 'active'

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'display_name': pytest.display_name}

    # Request
    response = app.test_client().put(f'/members/{member_uuid}', json=payload, headers=headers)

    # Response
    assert response.status_code == 400
