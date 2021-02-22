from .schema import MemberPendingSchema
from ..base import Base


class member_pending(Base):
    key = 'member_pending'
    schema = MemberPendingSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, member):
        data = cls.schema.dump({'member': member})
        return member_pending(data=data)
