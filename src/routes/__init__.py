from .v1 import AvatarsAPI
from .v1 import LeaguesAPI, LeaguesListAPI
from .v1 import MembersAPI, MembersListAPI, MembersLeaguesListAPI
from .v1 import PingAPI
from .. import api

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Leagues
api.add_resource(LeaguesAPI, '/leagues/<uuid:uuid>', endpoint="league")
api.add_resource(LeaguesListAPI, '/leagues', endpoint="leagues")
api.add_resource(MembersLeaguesListAPI, '/members/<uuid:uuid>/leagues', endpoint="member_leagues")

# Members
api.add_resource(MembersAPI, '/members/<uuid:uuid>', endpoint="member")
api.add_resource(MembersListAPI, '/leagues/<uuid:uuid>/members', '/members', endpoint="members")

# Avatars
api.add_resource(AvatarsAPI, '/leagues/<uuid>/avatars', endpoint="avatar")
