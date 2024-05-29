from flask import Flask, session
from config import config_map
import logging
from logging.handlers import RotatingFileHandler
import os
from redis import StrictRedis
from app.extensions import db, mail, csrf, migrate, session, apifairy
from flask_migrate import Migrate
from flask_cors import CORS

# redis 连接对象
redis_store = None

def register_logging(level):
    '''设置日志的记录等级'''
    # 业务逻辑开启后就加载日志
    logging.basicConfig(level=level)
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # 记录基础日志
    add_logging_handler()

    # 记录操作日志
    add_logging_handler('operation')

def add_logging_handler(name='base'):
    path = 'logs/%s.log' % name

    # 创建日志记录器，指明日志保存的路径，每日志文件最大大小，日志文件个数上限
    file_handler = RotatingFileHandler(path, maxBytes=1024*100, backupCount=10)
    # 设置日志记录的格式
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))

    logging.getLogger(name).addHandler(file_handler)

# 工厂模式创建 flask app 对象
def create_app():
    '''创建 flask app 对象'''

    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    config_name = os.getenv('FLASK_ENV', 'testing') # 默认为测试模式
    config_cls = config_map.get(config_name)
    # 设置flask app的配置信息
    app.config.from_object(config_cls)

    # 配置日志
    register_logging(config_map.get(config_name).LOGGING_LEVEL)

    # 初始化extension
    init_extensions(app)

    # 注册blueprints
    register_blueprints(app)

    if config_name != 'testing': 
        # 初始化 redis 连接对象
        global redis_store 
        redis_store = StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT,
                                        db=config_cls.REDIS_DB, password=config_cls.REDIS_PASSWORD)
        app.config['REDIS_STORE'] = redis_store
    return app

def register_blueprints(app):
    # 注册 api 蓝图
    from app.blueprints.api import api
    app.register_blueprint(api, url_prefix="/api")
    from app.blueprints.admin import admin 
    app.register_blueprint(admin)  
    from app.blueprints.token import token 
    app.register_blueprint(token)

def init_extensions(app):
    db.init_app(app) # 初始化数据库db
    # csrf.init_app(app)
    migrate.init_app(app, db) 
    session.init_app(app) # 将flask里的session数据保存到redis中
    mail.init_app(app)
    apifairy.init_app(app)  

    # flask-cors 解决跨域问题
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
