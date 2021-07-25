from marshmallow import Schema, fields, validate

class ReportSchema(Schema):
  project_id = fields.String()
  dedication_percentage = fields.Float()

class ReportDetailSchema(ReportSchema):
  doc_id = fields.String()
  iso_year = fields.Integer()
  iso_week = fields.Integer()
  created_at = fields.Date()
  updated_at = fields.Date()
