import datetime
from mongoengine import DateTimeField, Document

class DocumentMixin(Document):
  created_at = DateTimeField(default=datetime.datetime.utcnow)
  updated_at = DateTimeField(default=datetime.datetime.utcnow)

  meta = { 'allow_inheritance': True }

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def save(self, *args, **kwargs):
    self.updated_at = datetime.datetime.utcnow()
    super().save(*args, **kwargs)
