from .schema import MemberCreatedSchema
from ..base import Base


class member_created(Base):
    key = 'member_created'
    schema = MemberCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, member):
        data = cls.schema.dump({'member': member})
        return member_created(data=data)
