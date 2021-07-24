import modules.projects.serializers as serializers
from flask import request, Blueprint, jsonify, abort
from middlewares.schemas import parameters
from middlewares.auth import jwt_required
from modules.projects.models import Project
from modules.projects.utils import check_project_existance

project_blueprint = Blueprint('Project controller', __name__)

@project_blueprint.route('/', methods=['POST'])
@jwt_required
@parameters(schema=serializers.ProjectSchema())
def create():
  body = request.get_json()

  if check_project_existance(body['name']):
    abort(409, 'project exists')
  else:
    new_project = Project(**body)
    new_project.save()
    return jsonify({ 'message': 'project created' }), 200

@project_blueprint.route('/list', methods=['GET'])
@jwt_required
def projects_list():
  page = 1 if not 'page' in request.args else int(request.args.get['page'])
  items_per_page = 15
  offset = (page - 1) * items_per_page

  projects = Project.objects.skip(offset).limit(items_per_page)
  projects = serializers.ProjectDetailSchema(many=True).dump(projects)

  return jsonify({ 'projects': projects }), 200
