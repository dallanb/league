from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db
from ..common import MemberStatusEnum


class Member(db.Model, BaseMixin):
    user_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    league_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('league.uuid'), nullable=False)
    status = db.Column(db.Enum(MemberStatusEnum), db.ForeignKey('member_status.name'), nullable=False)

    # Relationship
    member_status = db.relationship("MemberStatus")
    league = db.relationship("League", back_populates="members", lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Member.register()
