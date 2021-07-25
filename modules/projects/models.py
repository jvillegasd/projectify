from modules.models import DocumentMixin
from modules.users.models import User
from mongoengine import *

class Project(DocumentMixin):
  name = StringField(required=True, unique)
  description = StringField(max_length=1250)
