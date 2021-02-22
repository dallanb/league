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

    def fetch_members(self, params):
        res = MemberExternal().fetch_members(params=params)
        return res['data']['members']

    def fetch_member(self, user_uuid, league_uuid=None):
        cache_key = user_uuid if not league_uuid else f'{user_uuid}_{league_uuid}'
        hit = self.cache.get(cache_key)
        if hit:
            return hit
        res = MemberExternal().fetch_member_user(uuid=user_uuid, params={'league_uuid': league_uuid})
        member = res['data']['members']
        self.cache.set(cache_key, member, 3600)
        return member

    def fetch_member_batch(self, uuids):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            members = executor.map(self.fetch_member, uuids)
        return members
