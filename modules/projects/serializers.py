from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
  name = fields.String(required=True)
  description = fields.String(validate=validate.Length(max=1250))

class ProjectDetailSchema(ProjectSchema):
  doc_id = fields.String()
  created_at = fields.Date()
  updated_at = fields.Date()

class ReportSchema(Schema):
  project_id = fields.String()
  dedication_percentage = fields.Float()

class ReportDetailSchema(ReportSchema):
  doc_id = fields.String()
  iso_year = fields.Integer()
  iso_week = fields.Integer()
  created_at = fields.Date()
  updated_at = fields.Date()
