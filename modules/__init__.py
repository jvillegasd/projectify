from environs import Env
from mongoengine import connect
from modules.users.controller import user_blueprint
from modules.projects.controller import project_blueprint

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
