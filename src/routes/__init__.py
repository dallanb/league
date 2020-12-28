from .v1 import AvatarsAPI
from .v1 import LeaguesAPI, LeaguesListAPI
from .v1 import PingAPI
from .. import api

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Leagues
api.add_resource(LeaguesAPI, '/leagues/<uuid:uuid>', endpoint="league")
api.add_resource(LeaguesListAPI, '/leagues', endpoint="leagues")

# Avatars
api.add_resource(AvatarsAPI, '/leagues/<uuid>/avatars', endpoint="avatar")
