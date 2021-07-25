import uuid
import datetime
import modules.reports.serializers as serializers
from bson.objectid import ObjectId
from flask import request, Blueprint, jsonify, abort
from middlewares.schemas import parameters
from middlewares.auth import jwt_required
from modules.reports.models import Report
from modules.users.models import User
from modules.projects.models import Project
from modules.reports.utils import report_already_done, can_edit_report
from modules.utils.token import get_info_from_token

report_blueprint = Blueprint('Report controller', __name__)

@report_blueprint.route('/', methods=['POST'])
@jwt_required
@parameters(schema=serializers.ReportSchema())
def create():
  body = request.get_json()
  auth_header = request.headers['Authorization'].split('Bearer ')[1]
  decoded_token = get_info_from_token(auth_header)

  user = User.objects.filter(doc_id=decoded_token['doc_id']).first()
  project = Project.objects.filter(doc_id=body['project_id']).first()
  if not project:
    abort(404, 'project not found')

  if report_already_done(project, user, body['report_date']):
    abort(400, 'weekly report already done')
  else:
    report_date = datetime.datetime.strptime(body['report_date'], '%Y-%m-%d')
    new_report = Report(
      project=uuid.UUID(body['project_id']),
      user=uuid.UUID(decoded_token['doc_id']),
      report_date=report_date,
      dedication_percentage=body['dedication_percentage']
    )
    new_report.save()
    return jsonify({ 'message': 'report created' }), 200

@report_blueprint.route('/list', methods=['GET'])
@jwt_required
def reports_list():
  auth_header = request.headers['Authorization'].split('Bearer ')[1]
  decoded_token = get_info_from_token(auth_header)

  page = 1 if not 'page' in request.args else int(request.args.get['page'])
  items_per_page = 15
  offset = (page - 1) * items_per_page

  user = uuid.UUID(decoded_token['doc_id'])
  reports = Report.objects.filter(user=user)
  reports = reports.skip(offset).limit(items_per_page)
  reports = serializers.ReportDetailSchema(many=True).dump(reports)

  return jsonify({ 'reports': reports }), 200

@report_blueprint.route('/<report_id>', methods=['PUT'])
@jwt_required
@parameters(schema=serializers.ReportEditSchema())
def edit(report_id):
  body = request.get_json()
  
  if can_edit_report(report_id, body['edit_date']):
    db_report = Report.objects.filter(doc_id=report_id).first()
    db_report.dedication_percentage = body['dedication_percentage']
    db_report.save()
    return jsonify({ 'message': 'report updated' }), 200
  else:
    abort(400, 'report cannot be edited')
