from app import db
from marshmallow import Schema, fields, validate


class WeChatPaySchema(Schema):
    amount = fields.Number(required=True, validate=validate.Range(min=0.01))

class WeChatPayJSAPISchema(WeChatPaySchema):
    amount = fields.Number(required=True, validate=validate.Range(min=0.01))
    openid = fields.Str(required=True)
