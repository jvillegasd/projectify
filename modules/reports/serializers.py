import os
from flask import current_app
from marshmallow import Schema, fields, validate, pre_load
from marshmallow.exceptions import ValidationError
from modules.projects.serializers import ProjectDetailSchema

class ReportSchema(Schema):
  project_id = fields.String(required=True)
  report_date = fields.Date(required=True)
  dedication_percentage = fields.Float(required=True, 
                          validate=validate.Range(1, 100))

class ReportDetailSchema(ReportSchema):
  project = fields.Nested(ProjectDetailSchema(only=('doc_id', )))
  doc_id = fields.String()
  report_iso_year = fields.Integer()
  report_iso_week = fields.Integer()
  report_date = fields.Date()
  created_at = fields.Date()
  updated_at = fields.Date()

class ReportEditSchema(Schema):
  edit_date = fields.Date(required=True)
  dedication_percentage = fields.Float(required=True, 
                          validate=validate.Range(1, 100))

class UploadReportSchema(Schema):
  filename = fields.String(required=True)

  @pre_load
  def check_file_extension(self, data, **kwargs):
    filename = data['filename']
    if filename:
      file_ext = os.path.splitext(filename)[1]
      if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
        raise ValidationError('invalid file extension')
    
    return data

class RequestReportFile(Schema):
  start_date = fields.Date(required=True)
  end_date = fields.Date(required=True)
