import logging
from http import HTTPStatus

from .base import Base
from .. import app
from ..common.utils import s3_object_name, get_image_data
from ..libs import S3
from ..models import Avatar as AvatarModel


class Avatar(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.s3 = S3(aws_access_key_id=app.config['S3_ACCESS_KEY'], aws_secret_access_key=app.config['S3_SECRET_KEY'])
        self.avatar_model = AvatarModel

    def find(self, **kwargs):
        return Base.find(self, model=self.avatar_model, **kwargs)

    def create(self, **kwargs):
        avatar = self.init(model=self.avatar_model, **kwargs)
        return self.save(instance=avatar)

    def update(self, uuid, **kwargs):
        avatars = self.find(uuid=uuid)
        if not avatars.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=avatars.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        avatar = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=avatar)

    def destroy(self, uuid, ):
        avatars = self.find(uuid=uuid)
        if not avatars.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=avatars.items[0])

    def upload_file(self, filename):
        result = self.s3.upload(filename=filename, bucket=app.config['S3_BUCKET'],
                                object_name=s3_object_name(filename))
        if not result:
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return result

    def upload_fileobj(self, file, filename):
        file_obj = get_image_data(file=file)
        result = self.s3.upload_obj(
            file=file_obj,
            bucket=app.config['S3_BUCKET'],
            object_name=s3_object_name(filename),
            extra_args={
                "ACL": "public-read"
            }
        )
        if not result:
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return

    @staticmethod
    def generate_s3_filename(league_uuid):
        return f"{league_uuid}.jpeg"
