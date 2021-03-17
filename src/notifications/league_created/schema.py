from marshmallow import Schema, pre_dump
from webargs import fields


class LeagueCreatedSchema(Schema):
    uuid = fields.UUID(attribute='league.uuid')
    owner_uuid = fields.UUID(attribute='league.owner_uuid')

    @pre_dump
    def prepare(self, data, **kwargs):
        return data
