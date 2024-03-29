import logging
from http import HTTPStatus

from sqlalchemy.orm import joinedload

from src import app
from .base import Base
from ..decorators.notifications import league_notification
from ..models import League as LeagueModel, MemberMaterialized as MemberMaterializedModel


class League(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.league_model = LeagueModel
        self.max_members = int(app.config['MAX_MEMBERS'])

    def find(self, **kwargs):
        return self._find(model=self.league_model, **kwargs)

    @league_notification(operation='create')
    def create(self, **kwargs):
        league = self._init(model=self.league_model, **kwargs)
        return self._save(instance=league)

    def update(self, uuid, **kwargs):
        leagues = self.find(uuid=uuid)
        if not leagues.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=leagues.items[0], **kwargs)

    @league_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if league status is being updated we will trigger a notification
        league = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=league)

    def find_by_participant(self, user_uuid, user_status, include, paginate):
        query = self.league_model.query.add_entity(MemberMaterializedModel).filter(
            self.league_model.members.any(user_uuid=user_uuid, status=user_status))
        for key in include:
            query = query.options(joinedload(key))
        query = query.join(MemberMaterializedModel,
                           MemberMaterializedModel.league == self.league_model.uuid).filter(
            MemberMaterializedModel.user == user_uuid)
        return self.db.run_query(query=query, **paginate)

    # return True if limit is reached and False if not
    def check_members_limit(self, instance):
        grouped = instance.members_group_by(key_func=lambda x: x.status)
        # get the total number of members whose status is not inactive
        active = sum(len(list(g)) for k, g in grouped if k.value > 0)
        return active > self.max_members
