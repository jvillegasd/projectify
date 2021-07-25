import datetime
from modules.models import DocumentMixin
from modules.users.models import User
from modules.projects.models import Project
from mongoengine import *

class Report(DocumentMixin):
  project = ReferenceField(Project, required=True, dbref=False, reverse_delete_rule=CASCADE)
  user = ReferenceField(User, required=True, dbref=False, reverse_delete_rule=CASCADE)
  dedication_percentage = FloatField(required=True)
  report_date = DateTimeField(default=datetime.datetime.now)
  report_iso_year = IntField()
  report_iso_week = IntField()

  meta = {
    'indexes': [
        {'fields': (
            'project',
            'user',
            'report_iso_year',
            'report_iso_week'
          ), 
          'unique': True
        }
    ]
  }

  def save(self, *args, **kwargs):
    iso_date = self.report_date.isocalendar()
    if not self.report_iso_year:
      self.report_iso_year = iso_date[0]
    if not self.report_iso_week:
      self.report_iso_week = iso_date[1]
    
    super(Report, self).save(*args, **kwargs)
