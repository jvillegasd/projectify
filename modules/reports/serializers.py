from marshmallow import Schema, fields, validate
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
