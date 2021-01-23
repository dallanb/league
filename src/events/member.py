import logging

from ..services import MemberService


class Member:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()

    def handle_event(self, key, data):
        # this means a user has been updated from invited to active and data from member service can be used to
        # populate associated entry in member model
        if key == 'member_active':
            members = self.member_service.find(email=data['email'], league_uuid=data['league_uuid'], status='invited')
            if members.total:
                self.member_service.apply(instance=members.items[0], user_uuid=data['user_uuid'], status='pending')
