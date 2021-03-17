from .schema import MemberActiveSchema
from ..base import Base


class member_active(Base):
    key = 'member_active'
    schema = MemberActiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, member):
        data = cls.schema.dump({'member': member})
        return member_active(data=data)
