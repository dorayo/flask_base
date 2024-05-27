import re
from marshmallow import ValidationError


def validate_mobile(phone_number):
    """验证中国大陆的手机号码格式是否正确。"""
    if not re.match(r"^1[3-9]\d{9}$", phone_number):
        raise ValidationError("无效的手机号码。")
    
def validate_email(email):
    """验证电子邮件地址的格式是否正确。"""
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValidationError("无效的电子邮件地址。")

def validate_username(value):
    """
    验证用户名是否为字母数字组合，且长度在3到50字符之间。
    Args:
        value (str): 输入的用户名字符串。
    
    Raises:
        ValidationError: 如果输入不满足条件，则抛出验证错误。
    """
    if not 3 <= len(value) <= 50:
        raise ValidationError('用户名必须在3到50字符之间')
    if not re.match(r'^\w+$', value):
        raise ValidationError('用户名必须是字母数字组合')

def validate_password(value):
    """
    验证密码复杂性。密码必须至少包含6个字符，并且至少包括一个大写字母、一个小写字母和一个数字。
    Args:
        value (str): 输入的密码字符串。
    
    Raises:
        ValidationError: 如果密码不符合要求，则抛出验证错误。
    """
    if len(value) < 6:
        raise ValidationError('密码长度必须至少为6个字符')

    # 检查密码是否包含至少一个大写字母
    if not re.search(r'[A-Z]', value):
        raise ValidationError('密码必须包含至少一个大写字母')