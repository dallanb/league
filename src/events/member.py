import logging

from ..services import MemberService, MemberMaterializedService


class Member:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.member_materialized_service = MemberMaterializedService()

    def handle_event(self, key, data):
        # this means a user has been updated from invited to active and data from member service can be used to
        # populate associated entry in member model
        if key == 'member_active':
            members = self.member_service.find(email=data['email'], league_uuid=data['league_uuid'], status='invited')
            if members.total:
                self.member_service.apply(instance=members.items[0], user_uuid=data['user_uuid'], status='pending')
        # I need to handle avatar updates in member
        elif key == 'avatar_created':
            self.logger.info('avatar created')
            members = self.member_materialized_service.find(member=data['member_uuid'])
            if members.total:
                member = members.items[0]
                self.member_materialized_service.apply(instance=member, avatar=data['s3_filename'])
