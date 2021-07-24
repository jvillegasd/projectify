from modules.models import DocumentMixin
from modules.users.models import User
from mongoengine import *

class Project(DocumentMixin):
  name = StringField(required=True, unique=True)
  description = StringField(max_length=1250)

class Report(DocumentMixin):
  project_id = ReferenceField(Project, required=True, reverse_delete_rule=CASCADE)
  user_id = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
  dedication_percentage = FloatField(required=True)
  iso_year = IntField()
  iso_week = IntField()

  def save(self, *args, **kwargs):
    iso_date = datetime.datetime.now().isocalendar()
    if not self.iso_year:
      self.iso_year = iso_date[0]
    if not self.iso_week:
      self.iso_week = iso_date[1]
    
    super(Report, self).save(*args, **kwargs)
