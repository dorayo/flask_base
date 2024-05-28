from . import api
from flask import request, current_app
from app.utils.api_utils import RET, json_response, handle_api_call
from app.services import wechatpay_service
from app.services.auth_service import token_auth
from app.schemas.wechatpay_schemas import WeChatPaySchema

@api.route('/wechatpay', methods=['POST'])
@handle_api_call
def wechat_h5_pay():
    """
    h5发起支付
    """
    schema = WeChatPaySchema()
    data = schema.load(request.json)
    payer_client_ip = data.get('payer_client_ip')
    amount = data.get('amount')
    description = data.get('description')
    h5_info_type = data.get('h5_info_type')
    try:
        # 判断是否成功获取h5_url
        h5_url = wechatpay_service.h5_pay(payer_client_ip, amount, description, h5_info_type)
        if not h5_url:
            return json_response(RET.THIRDERR)
        return json_response(code=RET.OK, data=h5_url)
    except Exception as e:
        current_app.logger.error(f"微信支付错误: {e}")
        return json_response(code=RET.SERVERERR, detailMsg="微信支付错误")
    

@api.route('/wechatpay/notify', methods=['POST'])
@handle_api_call
def wechat_pay_notify():
    """
    微信支付通知接口
    """
    result = wechatpay_service.notify(request)
    if not result:
        err_message = {  
            "code": "FAIL",
            "message": "失败"
        }
        return json_response(code=RET.SERVERERR,data=err_message)
    return json_response(code=RET.OK)

