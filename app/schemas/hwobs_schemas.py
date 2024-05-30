from app import db
from marshmallow import Schema, fields, validate
from app.utils.validation_utils import validate_mobile,validate_code

class HWOBSSchema(Schema):
    file = fields.Raw(required=True)
