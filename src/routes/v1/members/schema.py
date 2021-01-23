from marshmallow import Schema, post_dump
from webargs import fields


class CreateMemberSchema(Schema):
    user_uuid = fields.UUID(required=False)
    email = fields.Email(required=True)


class DumpMemberSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    user_uuid = fields.UUID()
    league_uuid = fields.UUID()

    def get_attribute(self, obj, attr, default):
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class FetchMemberSchema(Schema):
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllMemberSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    user_uuid = fields.UUID(required=False)


create_schema = CreateMemberSchema()
dump_schema = DumpMemberSchema()
dump_many_schema = DumpMemberSchema(many=True)
fetch_schema = FetchMemberSchema()
fetch_all_schema = FetchAllMemberSchema()
