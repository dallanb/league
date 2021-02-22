from .mixins import BaseMixin
from .. import db


class Avatar(db.Model, BaseMixin):
    s3_filename = db.Column(db.String, nullable=False)

    # Relationship
    league = db.relationship("League", back_populates="avatar", uselist=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Avatar.register()
