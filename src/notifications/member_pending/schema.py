from marshmallow import Schema, pre_dump
from webargs import fields


class MemberPendingSchema(Schema):
    uuid = fields.UUID(attribute='member.uuid')
    user_uuid = fields.UUID(attribute='member.user_uuid')
    league_uuid = fields.UUID(attribute='member.league_uuid')
    email = fields.String(attribute='member.email')
    owner_uuid = fields.UUID(attribute='league.owner_uuid')
    message = fields.String(missing=None)

    @pre_dump
    def prepare(self, data, **kwargs):
        league = data['member'].league
        data['message'] = f"You have been invited to join {league.name}"
        data['league'] = league
        return data
