from . import api
from flask import request, current_app
from app.utils.api_utils import RET, json_response, handle_api_call
from app.services import hwsms_service
from app.schemas.hwsms_schemas import HWSMSSchema,HWSMSVerifySchema
from app.services import hwsms_service
from app.services.auth_service import token_auth

@api.route('/send_sms', methods=['POST'])
@handle_api_call
# @token_auth.login_required
def send_sms_hw():
  """
  发送短信
  """
  schema = HWSMSSchema()
  data = request.json
  data = schema.load(request.json)
  mobile = data.get('mobile')
  resp,code = hwsms_service.send_sms(mobile)
  redis_store = current_app.config['REDIS_STORE']  # 从 app 配置中获取 redis_store
  if resp:
    print("xxxxxx",redis_store)
    redis_store.setex(f'sms_code:{mobile}', 300, code)
    return json_response(code=RET.OK,data=code)
  else:
    return json_response(code=RET.SERVERERR)
  

@api.route('/verify_code', methods=['POST'])
@handle_api_call
# @token_auth.login_required
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
  redis_store = current_app.config['REDIS_STORE']  # 从 app 配置中获取 redis_store
  stored_code = redis_store.get(f'sms_code:{mobile}')
  if stored_code and stored_code.decode('utf-8') == input_code:
    return json_response(code=RET.OK)
  else:
    return json_response(code=RET.AUTHERR,detailMsg='验证码错误')