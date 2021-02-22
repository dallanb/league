import json

from src import app


#############
# SUCCESS
#############

###########
# Fetch
###########
def test_fetch_ping(reset_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'ping' is requested
    THEN check that the response is valid
    """
    # Request
    response = app.test_client().get(f'/ping')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
