import base64
import uuid as UUID
from io import BytesIO
from time import time

from .. import app


def generate_hash(items):
    frozen = frozenset(items)
    return hash(frozen)


def time_now():
    return int(time() * 1000.0)


def add_years(t, years=0):
    return t + 31104000000 * years


def generate_uuid():
    return UUID.uuid4()


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def file_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1]


def allowed_file(filename):
    return file_extension(filename) in app.config["ALLOWED_EXTENSIONS"]


def s3_object_name(filename):
    return f"{app.config['S3_FILEPATH']}{filename}"


def get_image_data(file):
    starter = file.find(',')
    image_data = file[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    return BytesIO(base64.b64decode(image_data))
