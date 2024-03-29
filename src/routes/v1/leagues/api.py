from flask import request, g
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import check_user, assign_user
from ....common.response import DataResponse
from ....services import LeagueService, MemberService, MemberMaterializedService


class LeaguesAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.league = LeagueService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        leagues = self.league.find(uuid=uuid, **data)
        if not leagues.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'leagues': self.dump(
                    schema=dump_schema,
                    instance=leagues.items[0],
                    params={
                        'include': data['include'],
                        'expand': data['expand']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        league = self.league.update(uuid=uuid, **data)
        return DataResponse(
            data={
                'leagues': self.dump(
                    schema=dump_schema,
                    instance=league
                )
            }
        )


class LeaguesListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.league = LeagueService()
        self.member = MemberService()
        self.member_materialized = MemberMaterializedService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        leagues = self.league.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=leagues.total,
                    page_count=len(leagues.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'leagues': self.dump(
                    schema=dump_many_schema,
                    instance=leagues.items,
                    params={
                        'include': data['include'],
                        'expand': data['expand']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self):
        data = self.clean(schema=create_schema, instance=request.get_json())

        owner = self.member.fetch_member(user_uuid=str(g.user))
        if owner is None:
            self.throw_error(http_code=self.code.BAD_REQUEST, msg='User not found')

        league = self.league.create(status='active', owner_uuid=g.user, name=data['name'])

        member = self.member.create(email=owner['email'], user_uuid=g.user, league=league, status='invited')
        # Todo: consider creating this asynchronously via notify or create using threading
        _ = self.member_materialized.create(uuid=member.uuid, username=owner['username'],
                                            display_name=owner['display_name'],
                                            user=owner['user_uuid'], email=owner['email'],
                                            member=None, league=league.uuid,
                                            country=owner['country'], status='invited')
        return DataResponse(
            data={
                'leagues': self.dump(
                    schema=dump_schema,
                    instance=league
                )
            }
        )


class MemberUserLeaguesListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.league = LeagueService()

    @marshal_with(DataResponse.marshallable())
    @assign_user
    def get(self, user_uuid):
        data = self.clean(schema=fetch_member_user_leagues_schema, instance={**request.args,
                                                                             'user_uuid': user_uuid})  # not cleaning user_uuid at base request level so make sure it is cleaned here
        leagues = self.league.find_by_participant(user_uuid=data['user_uuid'], user_status=data['member_status'], include=data['include'],
                                                  paginate=
                                                  {'page': data['page'], 'per_page': data['per_page']})
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=leagues.total,
                    page_count=len(leagues.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'leagues': self.dump(
                    schema=dump_many_member_user_schema,
                    instance=leagues.items,
                    params={
                        'include': data['include'],
                        'expand': data['expand']
                    }
                )
            }
        )
