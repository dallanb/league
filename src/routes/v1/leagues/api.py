from flask import request, g
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import check_user
from ....common.response import DataResponse
from ....services import LeagueService


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
        league = self.league.create(status='active', owner_uuid=g.user, name=data['name'])
        return DataResponse(
            data={
                'leagues': self.dump(
                    schema=dump_schema,
                    instance=league
                )
            }
        )