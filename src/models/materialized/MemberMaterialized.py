from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType, EmailType

from ... import db
from ...common import MemberStatusEnum
from ...common.utils import camel_to_snake, time_now


class MemberMaterialized(db.Model):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    uuid = db.Column(UUIDType(binary=False), primary_key=True, unique=True, nullable=False)
    ctime = db.Column(db.BigInteger, default=time_now)
    mtime = db.Column(db.BigInteger, onupdate=time_now)
    display_name = db.Column(db.String, nullable=True)
    email = db.Column(EmailType, nullable=False)
    username = db.Column(db.String, nullable=True)
    user = db.Column(UUIDType(binary=False), nullable=True)
    member = db.Column(UUIDType(binary=False), nullable=True)
    league = db.Column(UUIDType(binary=False), nullable=False)
    country = db.Column(db.String, nullable=True)
    avatar = db.Column(db.String, nullable=True)

    #FK
    status = db.Column(db.Enum(MemberStatusEnum), db.ForeignKey('member_status.name'), nullable=False)

    # Relationship
    member_status = db.relationship("MemberStatus")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
