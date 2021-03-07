from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import assign_user
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
            if members is None:
                self.throw_error(http_code=self.code.NOT_FOUND, msg='This user was not found')
            if len(members):
                self.throw_error(http_code=self.code.BAD_REQUEST,
                                 msg='This user already exists, please pass their user_uuid')

            existing_member = {}
        else:
            existing_member = self.member.fetch_member(user_uuid=str(data['user_uuid']))
            if existing_member is None:
                self.throw_error(http_code=self.code.NOT_FOUND, msg='This user was not found')

        member = self.member.create(user_uuid=data['user_uuid'], email=data['email'], league=leagues.items[0],
                                    status='invited')
        _ = self.member_materialized.create(uuid=member.uuid,
                                            username=existing_member.get('username', None),
                                            display_name=existing_member.get('display_name', None),
                                            email=data['email'],
                                            user=existing_member.get('user_uuid', None),
                                            member=None, status='invited',
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


class MembersMaterializedUserAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member_materialized = MemberMaterializedService()

    @marshal_with(DataResponse.marshallable())
    @assign_user
    def get(self, user_uuid):
        data = self.clean(schema=fetch_materialized_user_schema, instance={**request.args, 'user_uuid': user_uuid})
        members = self.member_materialized.find(**data)
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
        members = self.member_materialized.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=members.total,
                    page_count=len(members.items),
                    page=data.get('page', None),
                    per_page=data.get('per_page', None)),
                'members': self.dump(
                    schema=dump_many_materialized_schema,
                    instance=members.items,
                )
            }
        )
