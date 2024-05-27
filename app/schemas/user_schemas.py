from marshmallow import Schema, fields, validate, ValidationError, validates, validates_schema
import re
from app import db
from app.constants import APP_NORMAL_LIST_PAGE_COUNT, ROLES_LIST 
from app.models.user import User
from app.utils.validation_utils import validate_email, validate_mobile, validate_password, validate_username

class UserRegisterSchema(Schema):
    username = fields.Str(required=False, allow_none=True, validate=validate_username)
    mobile = fields.Str(required=True, validate=validate_mobile)
    email = fields.Email(required=False, allow_none=True, validate=validate_email)
    password = fields.Str(required=True, validate=validate_password)
    code = fields.Str(required=True, validate=validate.Length(equal=6))
    roles = fields.List(fields.Str(), required=False, load_default=['User']) # 默认为['User']

    @validates('mobile')
    def check_mobile_existence(self, value):
        # 检查手机号是否已经注册
        if db.session.query(User).filter(User.mobile == value).first():
            raise ValidationError("手机号已注册")

    @validates('email')
    def check_email_existence(self, value):
        # 检查电子邮件是否已被使用
        if db.session.query(User).filter(User.email == value).first():
            raise ValidationError("邮箱已注册")

    @validates('roles')
    # 不允许出现 'Admin' 角色
    def check_admin_role(self, value):
        if 'Admin' in value:
            raise ValidationError("Admin role is not allowed")

class AdminUserRegisterSchema(UserRegisterSchema):
    code = fields.Str(required=False)

    @validates('roles')
    def check_admin_role(self, value):
        # 管理员可以指定任何角色，包括 'Admin'
        # 角色只能是已存在的角色 
        for role in value:
            if role not in ROLES_LIST:
                raise ValidationError(f"Role {role} does not exist") 
        

class MobileLoginSchema(Schema):
    mobile = fields.String(required=True, validate=validate_mobile)
    device = fields.String(required=False)
    version = fields.String(required=False)
    code = fields.String(required=True, validate=validate.Length(equal=6))

class AccountLoginSchema(Schema):
    account = fields.String(required=True)
    password = fields.String(required=True, validate=validate_password)
    device = fields.String(required=False)
    version = fields.String(required=False)

class UserQuerySchema(Schema):
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=APP_NORMAL_LIST_PAGE_COUNT, validate=validate.Range(min=1, max=100))
    search = fields.Str(load_default=None)

class UserUpdateSchema(Schema):
    username = fields.Str(validate=[validate.Length(min=3, max=50)])
    email = fields.Email(validate=validate_email)
    avatar = fields.Url(allow_none=True)  # 允许为None，也就是可选参数
    status = fields.Int(validate=lambda x: x in [0, 1])  # 假设状态只能是0或1

    @validates_schema
    def validate_email(self, data, **kwargs):
        if 'email' in data:
            user = db.session.query(User).filter(User.email == data['email']).first()
            if user and user.id != data['id']:  # 假设请求中包含用户ID
                raise ValidationError("Email already in use by another account.", field_names=["email"])

class EmailSchema(Schema):
    email = fields.String(required=True, validate=validate_email)

class ResetPasswordSchema(Schema):
    mobile = fields.Str(required=True, validate=validate_mobile)
    repassword = fields.Str(required=True, validate=validate_password)

class ResetPasswordByEmailSchema(Schema):
    reset_token = fields.Str(required=True)
    repassword = fields.Str(required=True, validate=validate_password)

class PasswordChangeSchema(Schema):
    current_password = fields.Str(required=True, validate=validate_password)
    new_password = fields.Str(required=True, validate=validate_password)

    @validates('current_password')
    def validate_current_password(self, value):
        # 验证当前密码是否正确
        if not self.context['user'].check_password(value):
            raise ValidationError("Current password is incorrect")

    @validates('new_password')
    def validate_new_password(self, value):
        # 新密码不能与旧密码相同
        if value == self.context['current_password']:
            raise ValidationError("New password cannot be the same as the current password")
    
