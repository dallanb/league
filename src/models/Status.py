from ..common.enums import StatusEnum
from .. import db
from .mixins import EnumMixin


class Status(db.Model, EnumMixin):
    name = db.Column(db.Enum(StatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Status.register()
