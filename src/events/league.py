import logging

from ..services import LeagueService, MemberService, MemberMaterializedService


class League:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.league_service = LeagueService()
        self.member_service = MemberService()
        self.materialized_service = MemberMaterializedService()

    def handle_event(self, key, data):
        self.logger.info('league event')
        # this means a user has been updated from invited to active and data from league service can be used to
        # populate associated entry in league model
        if key == 'member_created':
            self.logger.info('member created')
            self.logger.info(data['user_uuid'])
            self.logger.info(data['owner_uuid'])
            # if the user is the owner of the league then set the status to active
            if data['user_uuid'] == data['owner_uuid']:
                _ = self.member_service.update(uuid=data['uuid'], status='active')
        elif key == 'member_pending' or key == 'member_active' or key == 'member_inactive':
            self.logger.info('member updated')
            status = key.split('member_')[1]
            member = self.member_service.fetch_member(user_uuid=data['user_uuid'], league_uuid=data['league_uuid'])
            _ = self.materialized_service.update(uuid=data['uuid'], username=member['username'],
                                                 display_name=member['display_name'],
                                                 email=member['email'], user=member['user_uuid'], member=member['uuid'],
                                                 country=member['country'], status=status)
