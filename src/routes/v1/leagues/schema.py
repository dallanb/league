from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields

from ....common import StatusEnum


class CreateLeagueSchema(Schema):
    name = fields.String()


class DumpLeagueSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    owner_uuid = fields.UUID()
    name = fields.String()
    status = EnumField(StatusEnum)

    def get_attribute(self, obj, attr, default):
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class UpdateLeagueSchema(Schema):
    name = fields.Str(required=False)


class FetchLeagueSchema(Schema):
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllLeagueSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    owner_uuid = fields.UUID(required=False)


create_schema = CreateLeagueSchema()
dump_schema = DumpLeagueSchema()
dump_many_schema = DumpLeagueSchema(many=True)
update_schema = UpdateLeagueSchema()
fetch_schema = FetchLeagueSchema()
fetch_all_schema = FetchAllLeagueSchema()
