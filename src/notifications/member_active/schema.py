from marshmallow import Schema, pre_dump
from webargs import fields


class MemberActiveSchema(Schema):
    uuid = fields.UUID(attribute='member.uuid')
    user_uuid = fields.UUID(attribute='member.user_uuid')
    league_uuid = fields.UUID(attribute='member.league_uuid')
    email = fields.String(attribute='member.email')
    owner_uuid = fields.UUID(attribute='league.owner_uuid')
    message = fields.String(missing=None)

    @pre_dump
    def prepare(self, data, **kwargs):
        member = data['member']
        league = data['member'].league
        external_member = self.service.fetch_member(user_uuid=str(member.user_uuid),
                                                    league_uuid=str(member.league_uuid))
        data['message'] = f"{external_member['display_name']} accepted invite to {league.name}"
        data['league'] = league
        return data
