from marshmallow import Schema, post_dump, pre_load
from marshmallow_enum import EnumField
from webargs import fields

from src.common import MemberStatusEnum


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
    status = EnumField(MemberStatusEnum)
    avatar = fields.String()
    league = fields.UUID()
    username = fields.String()
    display_name = fields.String()
    email = fields.Email()
    user = fields.UUID()
    member = fields.UUID()
    country = fields.String()


class UpdateMemberSchema(Schema):
    status = fields.Str(required=False)


class FetchMemberSchema(Schema):
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchMaterializedUserSchema(Schema):
    user = fields.UUID(required=True, data_key="user_uuid")
    league = fields.UUID(required=False, data_key="league_uuid", missing=None)


class FetchAllMemberSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    user_uuid = fields.UUID(required=False)


class _FetchAllMemberMaterializedSchemaCompareBy(Schema):
    status = fields.Int()


class FetchAllMemberMaterializedSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    sort_by = fields.String(required=False)
    league = fields.UUID(required=False, data_key="league_uuid")
    status = fields.String(required=False)
    compare_by = fields.Dict(fields.Str(), fields.Int())

    @pre_load
    def compare_by_handler(self, data, **kwargs):
        mutable_dict = data.to_dict()
        compare_by_list = [k for k in mutable_dict if k.split('.')[0] == 'compare_by']
        for compare_by in compare_by_list:
            val = mutable_dict.pop(compare_by)
            if not mutable_dict.get('compare_by', None):
                mutable_dict['compare_by'] = {}
            mutable_dict['compare_by'][compare_by[11:]] = val
        return mutable_dict


create_schema = CreateMemberSchema()
dump_schema = DumpMemberSchema()
dump_many_schema = DumpMemberSchema(many=True)
dump_materialized_schema = DumpMemberMaterializedSchema()
dump_many_materialized_schema = DumpMemberMaterializedSchema(many=True)
update_schema = UpdateMemberSchema()
fetch_schema = FetchMemberSchema()
fetch_materialized_user_schema = FetchMaterializedUserSchema()
fetch_all_schema = FetchAllMemberSchema()
fetch_all_materialized_schema = FetchAllMemberMaterializedSchema()
