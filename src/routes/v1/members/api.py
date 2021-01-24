from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import MemberService, LeagueService, MemberMaterializedService


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

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        member = self.member.update(uuid=uuid, **data)
        return DataResponse(
            data={
                'members': self.dump(
                    schema=dump_schema,
                    instance=member
                )
            }
        )


class MembersListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member = MemberService()
        self.member_materialized = MemberMaterializedService()
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
            existing_member = {}
            status = 'invited'
        else:
            existing_member = self.member.fetch_member(user_uuid=str(data['user_uuid']))
            status = 'pending'

        member = self.member.create(user_uuid=data['user_uuid'], email=data['email'], league=leagues.items[0],
                                    status=status)
        _ = self.member_materialized.create(uuid=member.uuid,
                                            display_name=existing_member.get('display_name', None),
                                            email=data['email'],
                                            user=existing_member.get('user_uuid', None),
                                            member=existing_member.get('uuid', None), status=status,
                                            country=existing_member.get('country', None),
                                            league=leagues.items[0].uuid)
        return DataResponse(
            data={
                'members': self.dump(
                    schema=dump_schema,
                    instance=member
                )
            }
        )


class MembersMaterializedAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member_materialized = MemberMaterializedService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        members = self.member_materialized.find(uuid=uuid)
        if not members.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'members': self.dump(
                    schema=dump_materialized_schema,
                    instance=members.items[0],
                )
            }
        )


class MembersMaterializedListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member_materialized = MemberMaterializedService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_materialized_schema, instance=request.args)
        self.logger.info(data)
        members = self.member_materialized.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=members.total,
                    page_count=len(members.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'members': self.dump(
                    schema=dump_many_materialized_schema,
                    instance=members.items,
                )
            }
        )
