from modules.models import DocumentMixin
from mongoengine import *

class AsyncResult(DocumentMixin):
  job_id = StringField(required=True)
  object_name = StringField(required=True)
