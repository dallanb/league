from .v1 import AvatarsAPI
from .v1 import LeaguesAPI, LeaguesListAPI, MemberUserLeaguesListAPI
from .v1 import MembersAPI, MembersListAPI, MembersMaterializedAPI, MembersMaterializedListAPI, MembersMaterializedUserAPI
from .v1 import PingAPI
from .. import api

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Leagues
api.add_resource(LeaguesAPI, '/leagues/<uuid:uuid>', endpoint="league")
api.add_resource(LeaguesListAPI, '/leagues', endpoint="leagues")
api.add_resource(MemberUserLeaguesListAPI, '/members/leagues/user/<user_uuid>',
                 endpoint="member_user_leagues")  # user_uuid might be 'me' so we dont want to check if uuid here # going to have problems with this call when a user declines an invite to a league

# Members
api.add_resource(MembersMaterializedAPI, '/members/materialized/<uuid:uuid>', endpoint="member_materialized")
api.add_resource(MembersMaterializedUserAPI, '/members/materialized/user/<user_uuid>', endpoint="member_user_materialized")
api.add_resource(MembersMaterializedListAPI, '/members/materialized', endpoint="members_materialized")
api.add_resource(MembersAPI, '/members/<uuid:uuid>', endpoint="member")
api.add_resource(MembersListAPI, '/leagues/<uuid:uuid>/members', '/members', endpoint="members")

# Avatars
api.add_resource(AvatarsAPI, '/leagues/<uuid>/avatars', endpoint="avatar")
