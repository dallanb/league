from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import MemberService, LeagueService


class MembersAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member = MemberService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        members = self.member.find(uuid=uuid, **data)
        if not members.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'members': self.dump(
                    schema=dump_schema,
                    instance=members.items[0],
                    params={
                        'expand': data['expand']
                    }
                )
            }
        )


class MembersListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member = MemberService()
        self.league = LeagueService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        members = self.member.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=members.total,
                    page_count=len(members.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'members': self.dump(
                    schema=dump_many_schema,
                    instance=members.items,
                    params={
                        'expand': data['expand']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.get_json())
        leagues = self.league.find(uuid=uuid)
        if not leagues.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        # if the user does not include user_uuid in the payload then we are too assume this user is not present in
        # the system
        if not data['user_uuid']:
            members = self.member.fetch_members(params={'email': data['email'], 'league_uuid': None})
            if len(members):
                self.throw_error(http_code=self.code.BAD_REQUEST,
                                 msg='This user already exists, please pass their user_uuid')
            status = 'invited'
        else:
            self.member.fetch_member(user_uuid=str(data['user_uuid']))
            status = 'pending'

        member = self.member.create(user_uuid=data['user_uuid'], email=data['email'], league=leagues.items[0],
                                    status=status)
        return DataResponse(
            data={
                'members': self.dump(
                    schema=dump_schema,
                    instance=member
                )
            }
        )
