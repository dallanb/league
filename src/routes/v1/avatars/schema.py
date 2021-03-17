from marshmallow import Schema, post_dump
from webargs import fields


class CreateAvatarSchema(Schema):
    avatar = fields.Field()


class DumpAvatarSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    s3_filename = fields.String()

    def get_attribute(self, obj, attr, default):
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class FetchAvatarSchema(Schema):
    s3_filename = fields.String()


dump_schema = DumpAvatarSchema()
dump_many_schema = DumpAvatarSchema(many=True)
fetch_schema = FetchAvatarSchema()
create_schema = CreateAvatarSchema()
