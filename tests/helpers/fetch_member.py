import pytest


def fetch_member(self, user_uuid, league_uuid=None):
    if user_uuid == str(pytest.user_uuid):
        return {
            "user_uuid": str(pytest.user_uuid),
            "uuid": str(pytest.member_uuid),
            "email": pytest.email,
            "status": "active",
            "display_name": pytest.display_name,
            "league_uuid": pytest.league.uuid,
            "username": pytest.username,
            "country": pytest.country
        }
    else:
        return None
