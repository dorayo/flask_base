from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from app.constants import ACTIVE_USER_BEFORE_DAY
from datetime import datetime, timedelta
import base64
import os

class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')  
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间') 

class TokenBaseModel(BaseModel):
    token = db.Column(db.String(32), index=True, unique=True, comment='token')
    token_expiration = db.Column(db.DateTime, nullable=True, comment='token 过期时间')   # token 过期时间

    def get_token(self, expires_in=0, change=False):
        now = datetime.now()
        if not expires_in:
            expires_in = ACTIVE_USER_BEFORE_DAY * 24 * 60 * 60
        self.token_expiration = now + timedelta(seconds=expires_in)
        if not change and self.token:
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now() - timedelta(seconds=1)

class PasswordBaseModel(BaseModel):
    password = db.Column(db.String(102), nullable=True)

    def set_password(self, passwd):
        '''设置加密后的密码'''
        self.password = generate_password_hash(passwd)

    def check_password(self, passwd):
        '''检查密码的正确性'''
        return check_password_hash(self.password, passwd)