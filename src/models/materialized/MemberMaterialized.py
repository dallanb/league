from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType, EmailType

from ... import db
from ...common.utils import camel_to_snake, time_now


class MemberMaterialized(db.Model):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    uuid = db.Column(UUIDType(binary=False), primary_key=True, unique=True, nullable=False)
    ctime = db.Column(db.BigInteger, default=time_now)
    mtime = db.Column(db.BigInteger, onupdate=time_now)
    display_name = db.Column(db.String, nullable=False)
    email = db.Column(EmailType, nullable=False)
    user = db.Column(UUIDType(binary=False), nullable=True)
    member = db.Column(UUIDType(binary=False), nullable=True)
    status = db.Column(db.String, nullable=False)
    league = db.Column(UUIDType(binary=False), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
