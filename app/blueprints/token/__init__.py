from flask import Blueprint

# 创建一个Blueprint实例
token = Blueprint('token', __name__)

# 从当前目录导入路由定义
from . import tokens