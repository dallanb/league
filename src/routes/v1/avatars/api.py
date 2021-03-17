from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import check_user
from ....common.response import DataResponse
from ....services import AvatarService, LeagueService


class AvatarsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.avatar = AvatarService()
        self.league = LeagueService()

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.form)

        leagues = self.league.find(uuid=uuid, include=['avatar'])
        if not leagues.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        avatar = leagues.items[0].avatar

        s3_filename = self.avatar.generate_s3_filename(league_uuid=str(uuid))
        _ = self.avatar.upload_fileobj(file=data['avatar'], filename=s3_filename)
        if not avatar:
            avatar = self.avatar.create(s3_filename=s3_filename)
            self.league.apply(instance=leagues.items[0], avatar=avatar)
        return DataResponse(
            data={
                'avatars': self.dump(
                    schema=dump_schema,
                    instance=avatar
                )
            }
        )
