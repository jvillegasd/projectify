import jwt
from environs import Env

env = Env()
env.read_env()
JWT_KEY = env('SECRET_KEY')

def get_info_from_token(token):
  decoded_token = jwt.decode(token, JWT_KEY, algorithms='HS256')

  token_info = {
    'username': decoded_token['sub'],
    'name': decoded_token['name']
  }

  return token_info