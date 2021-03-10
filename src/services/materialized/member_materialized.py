import logging
from http import HTTPStatus

from ..base import Base
from ...models import MemberMaterialized as MaterializedModel


class MemberMaterialized(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.materialized_model = MaterializedModel

    def find(self, **kwargs):
        return self._find(model=self.materialized_model, **kwargs)

    def create(self, **kwargs):
        materialized_member = self._init(model=self.materialized_model, **kwargs)
        return self._save(instance=materialized_member)

    def update(self, uuid, **kwargs):
        materialized_members = self.find(uuid=uuid)
        if not materialized_members.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=materialized_members.items[0], **kwargs)

    def update_by_user(self, user, **kwargs):
        query = self.db.clean_query(model=self.materialized_model, user=user)
        return self._update(query=query, **kwargs)

    def apply(self, instance, **kwargs):
        materialized_member = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=materialized_member)
