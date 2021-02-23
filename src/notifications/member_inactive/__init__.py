from .schema import MemberInactiveSchema
from ..base import Base


class member_inactive(Base):
    key = 'member_inactive'
    schema = MemberInactiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, member):
        data = cls.schema.dump({'member': member})
        return member_inactive(data=data)
