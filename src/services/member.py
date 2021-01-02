import concurrent.futures
import logging
from http import HTTPStatus

from .base import Base
from ..decorators import member_notification
from ..external import Member as MemberExternal
from ..models import Member as MemberModel


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

    def fetch_member(self, user_uuid):
        hit = self.cache.get(user_uuid)
        if hit:
            return hit
        res = MemberExternal().fetch_members(params={'user_uuid': user_uuid, 'league_uuid': None, 'include': 'address'})
        member = res['data']['members'][0]
        self.cache.set(user_uuid, member, 3600)
        return member

    def fetch_member_batch(self, uuids):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            members = executor.map(self.fetch_member, uuids)
        return members
