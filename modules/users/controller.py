from flask import request, Blueprint, jsonify
from middlewares.schemas import parameters
from modules.users.serializers import CreateUserSchema
from modules.users.models import User

user_blueprint = Blueprint('User controller', __name__)

@user_blueprint.route('/', methods=['POST'])
@parameters(schema=CreateUserSchema())
def create():
  new_user = User(**request.get_json())
  new_user.save()
  return jsonify({ 'message': 'user created' }), 200
