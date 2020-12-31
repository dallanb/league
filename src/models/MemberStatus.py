from .mixins import EnumMixin
from .. import db
from ..common.enums import MemberStatusEnum


class MemberStatus(db.Model, EnumMixin):
    name = db.Column(db.Enum(MemberStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


MemberStatus.register()
