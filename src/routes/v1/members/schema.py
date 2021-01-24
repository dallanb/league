from marshmallow import Schema, post_dump
from webargs import fields


class CreateMemberSchema(Schema):
    user_uuid = fields.UUID(required=False, missing=None)
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


class DumpMemberMaterializedSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    name = fields.String()
    status = fields.String()
    avatar = fields.String()
    league = fields.UUID()
    display_name = fields.String()
    email = fields.Email()
    user = fields.UUID()
    member = fields.UUID()
    country = fields.String()


class FetchMemberSchema(Schema):
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllMemberSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    user_uuid = fields.UUID(required=False)


class FetchAllMemberMaterializedSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    sort_by = fields.String(required=False)
    league = fields.UUID(required=False, data_key="league_uuid")
    status = fields.String(required=False)


create_schema = CreateMemberSchema()
dump_schema = DumpMemberSchema()
dump_many_schema = DumpMemberSchema(many=True)
dump_materialized_schema = DumpMemberMaterializedSchema()
dump_many_materialized_schema = DumpMemberMaterializedSchema(many=True)
fetch_schema = FetchMemberSchema()
fetch_all_schema = FetchAllMemberSchema()
fetch_all_materialized_schema = FetchAllMemberMaterializedSchema
