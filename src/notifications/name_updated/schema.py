from marshmallow import Schema, pre_dump
from webargs import fields


class NameUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='league.uuid')
    name = fields.Str(attribute='league.name')

    @pre_dump
    def prepare(self, data, **kwargs):
        return data
