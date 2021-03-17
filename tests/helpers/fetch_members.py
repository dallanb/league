import logging

import pytest


def fetch_members(self, params):
    if params['email'] == pytest.email and (
            'league_uuid' not in params or params['league_uuid'] == str(pytest.league.uuid)):
        return [{
            "user_uuid": str(pytest.user_uuid),
            "uuid": str(pytest.member_uuid),
            "email": pytest.email,
            "status": "active",
            "display_name": pytest.display_name,
            "league_uuid": str(pytest.league.uuid),
            "username": pytest.username,
            "country": pytest.country
        }]
    else:
        return []
