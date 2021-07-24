# https://github.com/MongoEngine/extras-mongoengine/issues/8
import bcrypt
from environs import Env
from mongoengine import *

env = Env()
env.read_env()

class PasswordField(StringField):

  SALT_ROUNDS = int(env('SALT_ROUNDS'))

  def __init__(self, **kwargs):
    self.salt = bcrypt.gensalt(rounds=SALT_ROUNDS)
    super(PasswordField, self).__init__(kwargs)
  
  def set_password(self, password):
    password = bcrypt.hashpw(password, self.salt)
    return password
  
  def to_mongo(self, value):
    return self.set_password(value)
  
  def to_python(self, value):
    return value
  
  def to_dict(self, value):
    return {
      'salt': self.salt,
      'password': value
    }
