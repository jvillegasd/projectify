from marshmallow import Schema, fields

class CreateUserSchema(Schema):
  name = fields.String(required=True)
  username = fields.String(required=True)
  email = fields.String(required=True)
  password = fields.String(required=True)
