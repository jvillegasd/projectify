import datetime
from mongoengine import *
from modules.users.utils import PasswordField

class User(Document):
  name = StringField(required=True)
  username = StringField(required=True)
  email = EmailField(required=True)
  password = PasswordField(required=True)
  created_at = DateTimeField(default=datetime.datetime.utcnow)
  updated_at = DateTimeField(default=datetime.datetime.utcnow)

  def save(self, *args, **kwargs):
    self.updated_at = datetime.datetime.utcnow()
    super(User, self).save(*args, **kwargs)