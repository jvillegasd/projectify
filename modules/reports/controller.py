import os
import uuid
import datetime
import modules.reports.serializers as serializers
from flask import request, Blueprint, jsonify, abort, send_from_directory
from middlewares.schemas import parameters
from middlewares.auth import jwt_required
from modules.reports.models import Report
from modules.users.models import User
from modules.projects.models import Project
from modules.reports.utils import report_already_done, can_edit_report, \
  secure_file_save
from modules.utils.token import get_info_from_token
from jobs.reports import process_uploaded_document, generate_report_document
from jobs.utils import get_job_status

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

  page = 1 if not 'page' in request.args else int(request.args['page'])
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

@report_blueprint.route('/upload', methods=['POST'])
@jwt_required
@parameters(schema=serializers.UploadReportSchema())
def upload_records():
  auth_header = request.headers['Authorization'].split('Bearer ')[1]
  decoded_token = get_info_from_token(auth_header)
  uploaded_file = request.files['file']

  new_filename = secure_file_save(uploaded_file)
  job = process_uploaded_document.delay(new_filename, decoded_token['doc_id'])
  
  return jsonify({ 'job_id': job.id }), 200

@report_blueprint.route('/download', methods=['POST'])
@jwt_required
@parameters(schema=serializers.RequestReportFile())
def enqueue_download_records():
  body = request.get_json()
  job = generate_report_document.delay(**body)
  return jsonify({ 'job_id': job.id }), 200

@report_blueprint.route('/download/<job_id>', methods=['GET'])
@jwt_required
def download_records(job_id):
  from jobs.models import AsyncResult
  from utils import create_presigned_url_s3

  record = AsyncResult.objects.filter(job_id=job_id).first()
  job_status = get_job_status(job_id)
  
  if job_status == 'finished' or record:
    url = create_presigned_url_s3(record.object_name)
    if url:
      return jsonify({ 'file_url': url }), 200
    else:
      abort(404, 'file not found in s3 bucket')
  elif job_status != 'not_found':
    return jsonify({ 'message': job_status }), 202
  else:
    abort(404, 'job not found')
