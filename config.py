import os
import logging
from redis import StrictRedis

class Config(object):
    """应用程序默认配置类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'devkey^YHN7ujm')

    LOGGING_LEVEL = logging.DEBUG

    # APIFAIRY 配置
    APIFAIRY_TITLE = 'Flask_base Project'
    APIFAIRY_VERSION = '0.1.0'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite database for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = 'localhost:5000'  # 添加这行
    WTF_CSRF_ENABLED = False  # 禁用 CSRF 保护

class DevelopmentConfig(Config):
    """开发模式配置子类"""
    DEBUG = True
    # 数据库的配置信息 mysql
    mysql_host = os.getenv('DB_HOST', 'localhost')
    mysql_port = os.getenv('DB_PORT', '3306')
    mysql_database = os.getenv('DB_DATABASE', 'flask_base')
    mysql_username = os.getenv('DB_USERNAME', 'flask_base')
    mysql_password = os.getenv('DB_PASSWORD', '123456')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + mysql_username + ':' + mysql_password + '@' + mysql_host + ':' + mysql_port + '/' + mysql_database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    # SQLALCHEMY_ECHO = True # 是否显示SQL语句

    # redis 配置
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_DB = os.getenv('REDIS_DB', 1)
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

    # flask_session 配置信息
    SESSION_TYPE = "redis"  # 指明保存到redis中
    # SESSION_TYPE = "null"  
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                                db=REDIS_DB, password=REDIS_PASSWORD)
    SESSION_USE_SIGNER = True  # 对cookie中的session_id进行混淆处理
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24  # session的有效期(单位秒)

    # email 配置
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')

    # password reset 配置信息
    RESET_TOKEN_MINUTES = 30  # 重置密码token有效期(单位分钟)
    PASSWORD_RESET_URL = 'http://vchaoxi.com'

class ProductionConfig(DevelopmentConfig):
    """生产模式配置子类"""
    LOGGING_LEVEL = logging.INFO; 


config_map = {
    "development": DevelopmentConfig, # 开发模式
    "product": ProductionConfig,      # 生产/线上模式
    "testing": TestingConfig          # 测试模式
}


if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
