from .schema import LeagueInactiveSchema
from ..base import Base


class league_inactive(Base):
    key = 'league_inactive'
    schema = LeagueInactiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, league):
        data = cls.schema.dump({'league': league})
        return league_inactive(data=data)
