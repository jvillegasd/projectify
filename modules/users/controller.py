import jwt
import datetime
from environs import Env
from flask import request, Blueprint, jsonify, abort
from middlewares.schemas import parameters
from modules.users.serializers import CreateUserSchema, AuthTokenSchema
from modules.users.models import User
from modules.users.utils import check_user_existance

env = Env()
env.read_env()
JWT_KEY = env("SECRET_KEY")

user_blueprint = Blueprint('User controller', __name__)

@user_blueprint.route('/', methods=['POST'])
@parameters(schema=CreateUserSchema())
def create():
  body = request.get_json()

  if check_user_existance(body['username'], body['email']):
    abort(409, 'user exists')
  else:
    new_user = User(**body)
    new_user.save()
    return jsonify({ 'message': 'user created' }), 200

@user_blueprint.route('/token', methods=['POST'])
@parameters(schema=AuthTokenSchema())
def get_token():
  body = request.get_json()

  db_user = User.objects.filter(username=body['username']).first()
  if db_user and db_user.check_password(body['password']):
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=1)
    auth_token = jwt.encode({
      'sub': db_user.username,
      'name': db_user.name,
      'doc_id': str(db_user.doc_id),
      'exp': expiration_date,
      'iat': datetime.datetime.now(),
    }, JWT_KEY, algorithm='HS256')

    return jsonify({ 'token': f'Bearer {auth_token}' }), 200
  else:
    abort(400, 'bad credentials')
