import logging

from ..services import MemberService, MemberMaterializedService


class Member:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.member_materialized_service = MemberMaterializedService()

    def handle_event(self, key, data):
        if key == 'member_active':
            members = self.member_service.find(email=data['email'], league_uuid=data['league_uuid'])
            if members.total:
                member = members.items[0]
                self.member_service.apply(instance=member, user_uuid=data['user_uuid'],
                                          status='pending' if member.status.name == 'invited' else 'active')
        elif key == 'display_name_updated':
            members = self.member_materialized_service.find(member=data['uuid'])
            if members.total:
                member = members.items[0]
                self.member_materialized_service.apply(
                    instance=member,
                    name=data['display_name']
                )
        elif key == 'avatar_created':
            self.logger.info('avatar created')
            members = self.member_materialized_service.find(member=data['member_uuid'])
            if members.total:
                member = members.items[0]
                self.member_materialized_service.apply(instance=member, avatar=data['s3_filename'])
