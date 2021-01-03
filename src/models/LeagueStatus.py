from ..common.enums import LeagueStatusEnum
from .. import db
from .mixins import EnumMixin


class LeagueStatus(db.Model, EnumMixin):
    name = db.Column(db.Enum(LeagueStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


LeagueStatus.register()
