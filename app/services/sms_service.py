from app import redis_store
from flask import current_app
from datetime import datetime, timedelta
import random

def send_sms_code(mobile):
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    redis_store.set(f"sms_code:{mobile}", code, ex=300)  # 有效期设置为5分钟
    # 假设有一个函数 send_sms 用于发送短信
    # send_sms(mobile, f"Your verification code is: {code}")

def verify_sms_code(mobile, code, prefix):
    try:
        redis_sms_code = redis_store.get(f"{prefix}{mobile}")
        if redis_sms_code and str(redis_sms_code, 'utf-8') == code:
            return True
    except Exception as e:
        current_app.logger.error(f"Error verifying SMS code for mobile {mobile}: {str(e)}")
    return False

