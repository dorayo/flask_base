from . import api
from flask import request, current_app
from app.utils.api_utils import RET, json_response, handle_api_call
from app.services import wechatpay_service
from app.services.auth_service import token_auth
from app.schemas.wechatpay_schemas import WeChatPaySchema,WeChatPayJSAPISchema

@api.route('/wechat/pay/native', methods=['POST'])
@handle_api_call
def wechat_native_pay():
    """
    二维码支付
    """
    schema = WeChatPaySchema()
    data = schema.load(request.json)
    amount = data.get('amount')
    try:
        # 判断是否成功获取h5_url
        res = wechatpay_service.native_pay(amount)
        if not res:
            return json_response(RET.THIRDERR)
        return json_response(code=RET.OK, data=res)
    except Exception as e:
        current_app.logger.error(f"微信支付错误: {e}")
        return json_response(code=RET.SERVERERR, detailMsg="微信支付错误")
    

@api.route('/wechat/pay/jsapi', methods=['POST'])
@handle_api_call
def wechat_jsapi_pay():
    """
    小程序发起支付
    """
    print(request.json)
    schema = WeChatPayJSAPISchema()
    data = schema.load(request.json)
    amount = data.get('amount')
    amount = round(float(amount) * 100)
    openid = data.get('openid')
    try:
        res = wechatpay_service.jsapi_pay(openid, amount)
        if not res:
            return json_response(RET.THIRDERR)
        return json_response(code=RET.OK, data=res)
    except Exception as e:
        current_app.logger.error(f"微信支付错误: {e}")
        return json_response(code=RET.SERVERERR, detailMsg="微信支付错误")


@api.route('/wechat/pay/notify', methods=['POST'])
@handle_api_call
def wechat_pay_notify():
    """
    微信支付通知
    """
    result = wechatpay_service.notify(request)
    if not result:
        return json_response(code=RET.SERVERERR)
    return json_response(code=RET.OK, data=result)

