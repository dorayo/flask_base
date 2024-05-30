"""
The 'api' blueprint handles the API for the app.
Specifically, this blueprint handles the following:
users 
"""
from flask import Blueprint

# 创建蓝图对象 api
api = Blueprint('api', __name__)

from . import users, sms,obs
