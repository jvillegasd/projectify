import bcrypt
import datetime
from mongoengine import *
from modules.models import DocumentMixin
from modules.users.utils import PasswordField

class User(DocumentMixin):
  name = StringField(required=True)
  username = StringField(required=True, unique=True)
  email = EmailField(required=True, unique=True)
  password = PasswordField(required=True)
  
  def check_password(self, value):
    return bcrypt.checkpw(value.encode('utf-8'),
                          self.password.encode('utf-8'))
