import os
from flask import current_app
from wechatpayv3 import WeChatPay, WeChatPayType
from random import sample
from string import ascii_letters, digits
import json
import uuid
import time
from flask import jsonify

MCHID = os.getenv('MCHID') # 微信支付商户号

private_key_path = 'app/utils/apiclient_key.pem'  # 商户证书私钥
if not os.path.exists(private_key_path):
    raise Exception(f"Private key file not found at {private_key_path}")
with open(private_key_path) as f:
    PRIVATE_KEY = f.read() 

CERT_SERIAL_NO = os.getenv('CERT_SERIAL_NO') # 商户证书序列号
APIV3_KEY = os.getenv('MCHKEY') # API v3密钥
APPID = os.getenv('APPID') # APPID，应用ID
NOTIFY_URL = 'https://www.xxxx.com/notify' # 回调地址
CERT_DIR = './cert' #微信支付平台证书缓存目录
PARTNER_MODE = False # 是否为服务商模式

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    partner_mode=PARTNER_MODE)

def native_pay(amount=1, description="无"):
    '''
    native支付方式
    '''
    out_trade_no = ''.join(sample(ascii_letters + digits, 8))
    amount = 1
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.NATIVE
    )
    if code == 200:
        return json.loads(message)
    else:
        current_app.logger.error(f"微信支付下单失败：{message}")
        return None

def jsapi_pay(openid,amount=1):
    '''
    JSApi支付方式
    '''
    out_trade_no = ''.join(sample(ascii_letters + digits, 8))
    payer = {'openid': openid}
    code, message = wxpay.pay(
        description="AI面相",
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.JSAPI,
        payer=payer
    )
    result = json.loads(message)
    if code in range(200, 300):
        prepay_id = result.get('prepay_id')
        timestamp = str(int(time.time()))
        noncestr = str(uuid.uuid4()).replace('-', '')
        package = 'prepay_id=' + prepay_id
        sign = wxpay.sign([APPID, timestamp, noncestr, package])
        signtype = 'RSA'
        data = {
            'appId': APPID,
            'timeStamp': timestamp,
            'nonceStr': noncestr,
            'package': 'prepay_id=%s' % prepay_id,
            'signType': signtype,
            'paySign': sign
        }
        current_app.logger.info(f"微信支付下单：{data}")
        return data

    else:
        data = {
            'message': result.get('code')
        }
        return data


def notify(request):
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
