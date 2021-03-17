from itertools import groupby

from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types import TSVectorType

from .mixins import BaseMixin
from .. import db
from ..common import LeagueStatusEnum


class League(db.Model, BaseMixin):
    owner_uuid = db.Column(UUIDType(binary=False), nullable=False)
    name = db.Column(db.String, nullable=False)

    # Search
    search_vector = db.Column(TSVectorType('name'))

    # FK
    status = db.Column(db.Enum(LeagueStatusEnum), db.ForeignKey('league_status.name'), nullable=False)
    avatar_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('avatar.uuid'), nullable=True)

    # Relationship
    league_status = db.relationship("LeagueStatus")
    avatar = db.relationship("Avatar")
    members = db.relationship("Member", back_populates="league")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def members_group_by(self, key_func):
        members = self.members
        return groupby(members, key_func)


League.register()
