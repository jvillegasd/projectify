from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
  name = fields.String(required=True)
  description = fields.String(validate=validate.Length(max=1250))

class ProjectDetailSchema(ProjectSchema):
  doc_id = fields.String()
  created_at = fields.Date()
  updated_at = fields.Date()
