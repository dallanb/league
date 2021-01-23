from ..common.enums import MemberStatusEnum
from .. import db
from .mixins import EnumMixin


class MemberStatus(db.Model, EnumMixin):
    name = db.Column(db.Enum(MemberStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


MemberStatus.register()
