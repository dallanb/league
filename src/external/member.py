from .base import Base
from .. import app


class Member(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['MEMBER_URL']

    def fetch_member(self, uuid):
        url = f'{self.base_url}/members/{uuid}'
        res = self.get(url=url)
        return res.json()

    def fetch_members(self, params=None):
        url = f'{self.base_url}/members'
        res = self.get(url=url, params=params)
        return res.json()
