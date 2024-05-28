from . import api
from flask import request, current_app
from app.utils.api_utils import RET, json_response, handle_api_call
from app.services import hwsms_service
from app.schemas.hwsms_schemas import HWSMSSchema,HWSMSVerifySchema
from app.services import hwsms_service
from app import redis_store
from app.services.auth_service import token_auth

@api.route('/send_sms', methods=['POST'])
@handle_api_call
@token_auth.login_required
def send_sms_hw():
  """
  发送短信
  """
  schema = HWSMSSchema()
  data = schema.load(request.json)
  mobile = data.get('mobile')
  if not mobile:
    return json_response(code=RET.PARAMERR,detailMsg="手机号不能为空")
  resp,code = hwsms_service.send_sms(mobile)
  if resp:
    redis_store.setex(f'sms_code:{mobile}', 300, code)
    return json_response(code=RET.OK,data=code)
  else:
    return json_response(code=RET.SERVERERR)
  

@api.route('/verify_code', methods=['POST'])
@handle_api_call
@token_auth.login_required
def verify_code():
  """
  验证短信
  """
  schema = HWSMSVerifySchema()
  data = schema.load(request.json)
  mobile = data.get('mobile')
  input_code  = data.get('code')
  if not mobile or not input_code:
    return json_response(code=RET.PARAMERR)
  stored_code = redis_store.get(f'sms_code:{mobile}')
  if stored_code and stored_code == input_code:
    return json_response(code=RET.OK)
  else:
    return json_response(code=RET.AUTHERR,detailMsg='验证码错误')