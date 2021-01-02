import logging
from http import HTTPStatus

from .base import Base
from ..decorators import member_notification
from ..models import Member as MemberModel
from ..external import Member as MemberExternal


class Member(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.member_model = MemberModel

    def find(self, **kwargs):
        return Base.find(self, model=self.member_model, **kwargs)

    @member_notification(operation='create')
    def create(self, **kwargs):
        member = self.init(model=self.member_model, **kwargs)
        return self.save(instance=member)

    def update(self, uuid, **kwargs):
        members = self.find(uuid=uuid)
        if not members.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=members.items[0], **kwargs)

    @member_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if member status is being updated we will trigger a notification
        member = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=member)

    def fetch_owner(self, user_uuid, league_uuid):
        members = self.fetch_members(user_uuid=user_uuid, league_uuid=league_uuid)
        if not len(members):
            self.error(code=HTTPStatus.BAD_REQUEST)
        return members[0]

    def fetch_members(self, **kwargs):
        # add caching to this api call
        res = MemberExternal().fetch_members(params={**kwargs})
        members = res['data']['members']
        return members

    # possibly turn this into a decorator (the caching part)
    def fetch_member(self, uuid):
        hit = self.cache.get(uuid)
        if hit:
            return hit
        res = MemberExternal().fetch_member(uuid=uuid)
        member = res['data']['members']
        self.cache.set(uuid, member, 3600)
        return member
