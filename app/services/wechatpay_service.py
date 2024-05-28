from flask import current_app
from wechatpayv3 import WeChatPay, WeChatPayType
from random import sample
from string import ascii_letters, digits


# 微信支付商户号
MCHID = '1230000109'

# 商户证书私钥，此文件不要放置在下面设置的CERT_DIR目录里。
# with open('path_to_key/apiclient_key.pem') as f:
#     PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '444F4864EA9B34415...'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'

# APPID，应用ID，服务商模式下为服务商应用ID，即官方文档中的sp_appid，也可以在调用接口的时候覆盖。
APPID = 'wxd678efh567hg6787'

# 回调地址，也可以在调用接口的时候覆盖。
NOTIFY_URL = 'https://www.xxxx.com/notify'

# 接入模式：False=直连商户模式，True=服务商模式。
PARTNER_MODE = False

wxpay = WeChatPay(
    mchid=MCHID,
    # private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    partner_mode=PARTNER_MODE)

def h5_pay(payer_client_ip,amount=1,description="无",h5_info_type="Wap"):
    '''
    微信H5支付下单
    '''
    out_trade_no = ''.join(sample(ascii_letters + digits, 8))
    scene_info = {
                'payer_client_ip': payer_client_ip,
                'h5_info': {
                    'type': h5_info_type
                }}
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': int(amount)},
        pay_type=WeChatPayType.H5,
        scene_info=scene_info
    )
    if code == 200:
        return message['code_url']
    else:
        current_app.logger.error(f"微信支付下单失败：{message}")
        return None

def notify(request):
    '''
        微信支付通知
    '''
    try:
        result = wxpay.callback(request.headers, request.data)
        if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
            resp = result.get('resource')
            appid = resp.get('appid')
            mchid = resp.get('mchid')
            out_trade_no = resp.get('out_trade_no')
            transaction_id = resp.get('transaction_id')
            trade_type = resp.get('trade_type')
            trade_state = resp.get('trade_state')
            trade_state_desc = resp.get('trade_state_desc')
            bank_type = resp.get('bank_type')
            attach = resp.get('attach')
            success_time = resp.get('success_time')
            payer = resp.get('payer')
            amount = resp.get('amount').get('total')
            return {'code': 'SUCCESS', 'message': '成功'}
        else:
            return {'code': 'FAILED', 'message': '失败'}
    except Exception as e:
        current_app.logger.error(f"微信支付通知失败：{e}")
        return None
