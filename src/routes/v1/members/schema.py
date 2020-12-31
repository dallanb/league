from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields

from ....common import MemberStatusEnum


class CreateMemberSchema(Schema):
    user_uuid = fields.UUID()


class DumpMemberSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    user_uuid = fields.UUID()
    status = EnumField(MemberStatusEnum)

    def get_attribute(self, obj, attr, default):
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class UpdateMemberSchema(Schema):
    status = fields.Str(required=True)


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
update_schema = UpdateMemberSchema()
fetch_schema = FetchMemberSchema()
fetch_all_schema = FetchAllMemberSchema()
