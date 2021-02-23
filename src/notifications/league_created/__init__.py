from .schema import LeagueCreatedSchema
from ..base import Base


class league_created(Base):
    key = 'league_created'
    schema = LeagueCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, league):
        data = cls.schema.dump({'league': league})
        return league_created(data=data)
