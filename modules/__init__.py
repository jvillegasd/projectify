from environs import Env
from mongoengine import connect

env = Env()
env.read_env()

connect(
  env('MONGODB_DATABASE'),
  host=env('MONGODB_SERVER'),
  port=int(env('MONGODB_PORT')),
  username=env('MONGODB_ROOT_USERNAME'),
  password=env('MONGODB_PASSWORD'),
  authentication_source='admin'
)
