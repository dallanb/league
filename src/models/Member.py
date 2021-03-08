from sqlalchemy_utils import UUIDType, EmailType

from .mixins import BaseMixin
from .. import db
from ..common import MemberStatusEnum


class Member(db.Model, BaseMixin):
    # Constraints
    __table_args__ = (db.UniqueConstraint('league_uuid', 'user_uuid', name='league_user'),
                      db.UniqueConstraint('league_uuid', 'email', name='league_email'),)

    email = db.Column(EmailType, nullable=False)
    user_uuid = db.Column(UUIDType(binary=False), nullable=True)

    # FK
    status = db.Column(db.Enum(MemberStatusEnum), db.ForeignKey('member_status.name'), nullable=False)
    league_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('league.uuid'), nullable=False)

    # Relationship
    member_status = db.relationship("MemberStatus")
    league = db.relationship("League", back_populates="members", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Member.register()
