import bcrypt
from environs import Env
from mongoengine import *

env = Env()
env.read_env()

class PasswordField(StringField):

  SALT_ROUNDS = int(env('SALT_ROUNDS'))

  def __init__(self, regex=None, **kwargs):
    self.salt = bcrypt.gensalt(rounds=PasswordField.SALT_ROUNDS)
    super(PasswordField, self).__init__(**kwargs)
  
  def __set_password(self, password):
    password = bcrypt.hashpw(password.encode('utf8'), self.salt)
    return password.decode('utf8')
  
  def to_mongo(self, value):
    return self.__set_password(value)
  
  def to_python(self, value):
    return value
  
  def to_dict(self, value):
    return {
      'salt': self.salt,
      'password': value
    }

def check_user_existance(username, email):
  from modules.users.models import User

  query = Q(username=username) | Q(email=email)
  db_users = User.objects.filter(query)
  return True if db_users else False