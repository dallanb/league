from marshmallow import Schema, pre_dump
from webargs import fields


class LeagueInactiveSchema(Schema):
    uuid = fields.UUID(attribute='league.uuid')
    owner_uuid = fields.UUID(attribute='league.owner_uuid')
    message = fields.Str(missing=None)

    @pre_dump
    def prepare(self, data, **kwargs):
        data['message'] = None
        return data
