from marshmallow import EXCLUDE, fields, validate
from app.extensions import ma

class RegisterSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=2, max=80))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8))
    address = fields.String(load_default=None, allow_none=True)

class LoginSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
