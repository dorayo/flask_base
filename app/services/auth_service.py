from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from app.models.user import User 
from app import db
from app.utils.api_utils import RET, json_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.query(User).filter(User.username == username).first()
    if user and user.check_password(password):
        return user
    return None  

@basic_auth.error_handler
def basic_auth_error():
    return json_response(RET.AUTHERR, detailMsg="Invalid username or password")

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token)

@token_auth.error_handler
def token_auth_error():
    return json_response(RET.SESSIONERR, detailMsg="Invalid or expired token")

