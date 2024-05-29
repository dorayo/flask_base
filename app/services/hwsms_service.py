# coding=utf-8
import urllib.parse
import urllib.request
import requests
from app.utils.apig_sdk import signer
import os
import random
from flask import current_app


def generate_verification_code(length=6):
    code = ''.join(random.choices('0123456789', k=length))
    return code

def send_sms(mobile):

    url = os.getenv('HW_SMS_URL') #APP接入地址(在控制台"应用管理"页面获取)+接口访问URI
    APP_KEY = os.getenv('HW_SMS_APP_KEY') #APP_Key
    APP_SECRET = os.getenv('HW_SMS_APP_SECRET') #APP_Secret
    sender = os.getenv('HW_SMS_SENDER') #国内短信签名通道号
    TEMPLATE_ID = os.getenv('HW_SMS_TEMPLATE_ID') #模板ID
    signature = os.getenv('HW_SMS_SIGNATURE') #签名名称
    # 必填,全局号码格式(包含国家码),示例:+86151****6789,多个号码之间用英文逗号分隔
    receiver = mobile #短信接收人号码

    # 选填,短信状态报告接收地址,推荐使用域名,为空或者不填表示不接收状态报告
    statusCallBack = ""

    code = generate_verification_code()
    TEMPLATE_PARAM =  f'["{code}"]'
    print("====")
    print(sender,receiver,TEMPLATE_ID,TEMPLATE_PARAM,statusCallBack,signature)
    formData = urllib.parse.urlencode({
        'from': sender,
        'to': receiver,
        'templateId': TEMPLATE_ID,
        'templateParas': TEMPLATE_PARAM,
        # 'statusCallback': statusCallBack,
        'signature': signature 
    }).encode('ascii')
    print("=====")
    print(formData)

    sig = signer.Signer()
    sig.Key = APP_KEY
    sig.Secret = APP_SECRET

    r = signer.HttpRequest("POST", url)
    r.headers = {"content-type": "application/x-www-form-urlencoded"}
    r.body = formData

    sig.Sign(r)
    # print(r.headers["X-Sdk-Date"])
    # print("=======")
    # print(r.headers["Authorization"])
    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body, verify=False)
    print(resp.status_code, resp.reason)
    print(resp.content)
    if resp.status_code == 200:
        return resp,code
    else:
        current_app.logger.error(f"短信发送失败：{resp}")
        return None,None

