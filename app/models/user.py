from .. import db
from datetime import datetime 
from app.utils.time_utils import datetime_to_string
import time
from flask import current_app 
import jwt

from .base import BaseModel, TokenBaseModel, PasswordBaseModel

# 用户与角色的多对多关系表
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

# 角色与权限的多对多关系表
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)


class User(TokenBaseModel, PasswordBaseModel, db.Model):
    """用户账号表"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # 用户ID
    username = db.Column(db.String(50), unique=True, nullable=True) # 用户名
    mobile = db.Column(db.String(15), unique=True)  # 手机号
    email = db.Column(db.String(50), unique=True, nullable=True) # 邮箱
    roles = db.relationship('Role', secondary=user_roles, back_populates='users')
    avatar = db.Column(db.String(150), default="", comment="用户头像")
    status = db.Column(db.SmallInteger, default=1)  # 账号状态  1-使用 0-禁用
    last_login_time = db.Column(db.DateTime)    # 最新登录时间
    
    @staticmethod
    def check_token(token):
        user = db.session.query(User).filter(User.token == token).first()
        if user is None or user.token_expiration < datetime.now():
            return None
        return user
    
    def generate_reset_token(self):
        key = current_app.config['SECRET_KEY'] 
        payload={
            'exp': time.time() + current_app.config['RESET_TOKEN_MINUTES'] * 60,
            'reset_email': self.email
        }
        encoded = jwt.encode(payload, key, algorithm="HS256")
        return encoded

    @staticmethod
    def verify_reset_token(reset_token):
        try:
            data = jwt.decode(reset_token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except jwt.PyJWTError:
            return
        return db.session.query(User).filter(User.email == data['reset_email']).first() 

    def to_dict(self):
        return {
            'id': self.id,
            'mobile': self.mobile,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'status': self.status
        }

    def to_detail(self):
        return {
            'id': self.id,
            'mobile': self.mobile,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'wechat': self.wechat,
            'status': self.status,
            'create_time': datetime_to_string(self.create_time)
        }

    def has_role(self, role_name):
        for role in self.roles:
            if role.role_name == role_name:
                return True
        return False

class UserLoginRecord(BaseModel, db.Model):
    """
    用户登录信息表
    """
    __tablename__ = 'user_login_record'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_login_time = db.Column(db.DateTime, comment='最新登录时间')
    device = db.Column(db.String(20), default="", comment="登录设备")
    version = db.Column(db.String(10), default="", comment="登录手机版本")

class Role(db.Model):
    """
    角色表
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_roles, back_populates='roles')
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles')

    def __repr__(self):
        return f'<Role {self.name}>'

class Permission(db.Model):
    """
    权限表
    """
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(50), unique=True, nullable=False)

    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions')

    def __repr__(self):
        return f'<Permission {self.name}>'