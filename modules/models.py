import uuid
import datetime
from mongoengine import DateTimeField, Document, UUIDField

class DocumentMixin(Document):
  doc_id = UUIDField(default=uuid.uuid4, primary_key=True)
  created_at = DateTimeField(default=datetime.datetime.utcnow)
  updated_at = DateTimeField(default=datetime.datetime.utcnow)

  meta = { 'abstract': True }

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def save(self, *args, **kwargs):
    self.updated_at = datetime.datetime.utcnow()
    super().save(*args, **kwargs)
