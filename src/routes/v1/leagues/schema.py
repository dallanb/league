from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields

from ..avatars.schema import DumpAvatarSchema
from ....common import LeagueStatusEnum


class CreateLeagueSchema(Schema):
    name = fields.String()


class DumpLeagueSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    owner_uuid = fields.UUID()
    name = fields.String()
    status = EnumField(LeagueStatusEnum)
    avatar = fields.Nested(DumpAvatarSchema)
    members = fields.List(fields.Nested('DumpMemberSchema'))

    def get_attribute(self, obj, attr, default):
        if attr == 'avatar':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'members':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('avatar', False) is None:
            del data['avatar']
        if data.get('members', False) is None:
            del data['members']
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


class FetchMemberUserLeagueSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    user_uuid = fields.UUID()


create_schema = CreateLeagueSchema()
dump_schema = DumpLeagueSchema()
dump_many_schema = DumpLeagueSchema(many=True)
update_schema = UpdateLeagueSchema()
fetch_schema = FetchLeagueSchema()
fetch_all_schema = FetchAllLeagueSchema()
fetch_member_user_leagues_schema = FetchMemberUserLeagueSchema()
