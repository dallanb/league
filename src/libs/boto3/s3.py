import logging
import boto3
from botocore.exceptions import ClientError


class S3:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)

    def upload(self, filename, bucket, object_name):
        try:
            self.client.upload_file(filename, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_obj(self, file, bucket, object_name, extra_args):
        try:
            self.client.upload_fileobj(file, bucket, object_name, ExtraArgs=extra_args)
        except ClientError as e:
            logging.error(e)
            return False
        return True
