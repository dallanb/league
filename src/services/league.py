import logging
from http import HTTPStatus

from .base import Base
from ..decorators import league_notification
from ..models import League as LeagueModel


class League(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.league_model = LeagueModel

    def find(self, **kwargs):
        return Base.find(self, model=self.league_model, **kwargs)

    @league_notification(operation='create')
    def create(self, **kwargs):
        league = self.init(model=self.league_model, **kwargs)
        return self.save(instance=league)

    def update(self, uuid, **kwargs):
        leagues = self.find(uuid=uuid)
        if not leagues.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=leagues.items[0], **kwargs)

    @league_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if league status is being updated we will trigger a notification
        league = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=league)

    def find_by_participant(self, filters, paginate):
        query = self.league_model.query.filter(
            self.league_model.members.any(**filters))
        return self.db.clean_query(query=query, **paginate)
