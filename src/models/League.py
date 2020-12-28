from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types import TSVectorType

from .mixins import BaseMixin
from .. import db
from ..common import StatusEnum


class League(db.Model, BaseMixin):
    owner_uuid = db.Column(UUIDType(binary=False), nullable=False)
    name = db.Column(db.String, nullable=False)

    # Search
    search_vector = db.Column(TSVectorType('name'))

    # FK
    status = db.Column(db.Enum(StatusEnum), db.ForeignKey('status.name'), nullable=False)

    # Relationship
    league_status = db.relationship("Status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


League.register()