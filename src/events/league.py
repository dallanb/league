import logging

from ..common import ManualException, MemberStatusEnum, time_now
from ..services import LeagueService, MemberService, MemberMaterializedService


class League:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.league_service = LeagueService()
        self.member_service = MemberService()
        self.materialized_service = MemberMaterializedService()

    def handle_event(self, key, data):
        self.logger.info('league event')
        if key == 'member_created':
            self.logger.info('member created')
        elif key == 'member_pending' or key == 'member_active' or key == 'member_inactive':
            self.logger.info('member updated')
            status = key.split('member_')[1]
            # we have to invalidate member cache since we know an update has just happened
            cache_key = self.member_service.get_member_cache_key(user_uuid=data['user_uuid'],
                                                                 league_uuid=data['league_uuid'])
            self.member_service.delete_member_cache(key=cache_key)
            member = self.member_service.fetch_member(user_uuid=data['user_uuid'], league_uuid=data['league_uuid'])
            if member is None:
                raise ManualException(
                    err=f'member with user_uuid: {data["user_uuid"]} and league_uuid: {data["league_uuid"]} not found')
            activation_time = time_now() if status == MemberStatusEnum.active.name else None
            _ = self.materialized_service.update(uuid=data['uuid'], username=member['username'],
                                                 display_name=member['display_name'],
                                                 email=member['email'], user=member['user_uuid'], member=member['uuid'],
                                                 country=member['country'], activation_time=activation_time,
                                                 status=status)
