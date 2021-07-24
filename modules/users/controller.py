from flask import request, Blueprint, jsonify
from middlewares.schemas import parameters
from modules.users.serializers import CreateUserSchema

user_blueprint = Blueprint('User controller', __name__)

@user_blueprint.route('/', methods=['POST'])
@parameters(schema=CreateUserSchema())
def create():
  return jsonify({ 'message': request.get_json() }), 200
