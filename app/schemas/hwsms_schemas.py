from app import db
from marshmallow import Schema, fields, validate
from app.utils.validation_utils import validate_mobile,validate_code

class HWSMSSchema(Schema):
    mobile = fields.Str(required=True, validate=validate_mobile)

class HWSMSVerifySchema(Schema):
    mobile = fields.Str(required=True, validate=validate_mobile)
    code = fields.Str(required=True, validate=validate_code)