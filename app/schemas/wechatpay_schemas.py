from app import db
from marshmallow import Schema, fields, validate, ValidationError, validates, validates_schema


class WeChatPaySchema(Schema):
    payer_client_ip = fields.Str(required=True, validate=validate.Regexp(
        r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
        error="Invalid IP address."
    ))
    amount = fields.Int(required=True, validate=validate.Range(min=1))
    description = fields.Str(required=False, validate=validate.Length(min=1))
    type = fields.Str(required=False, validate=validate.Length(min=1))
    h5_info_type = fields.Str(required=False, validate=validate.Length(min=1))
    