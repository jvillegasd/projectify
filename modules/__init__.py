from environs import Env
from mongoengine import connect
from modules.users.controller import user_blueprint
from modules.projects.controller import project_blueprint
from modules.reports.controller import report_blueprint

env = Env()
env.read_env()

connect(
  host=env('MONGODB_URL'),
  authentication_source='admin'
)