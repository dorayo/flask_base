from . import api
from flask import request, current_app
from app.utils.api_utils import RET, json_response, handle_api_call
from app.models.user import User 
from app.constants import SMS_REDIS_FORGET_PREFIX, SMS_REDIS_LOGIN_PREFIX, SMS_REDIS_REGISTER_PREFIX
from app import redis_store
from datetime import datetime
from app.utils.email import send_email
from app.schemas.user_schemas import AccountLoginSchema, EmailSchema, MobileLoginSchema, PasswordChangeSchema, ResetPasswordByEmailSchema, ResetPasswordSchema, UserRegisterSchema, UserUpdateSchema
from app.services.auth_service import token_auth
from app.services.sms_service import verify_sms_code
from app.services import user_service


@api.route('/users', methods=['POST'])
@handle_api_call
def register():
    """
    注册新用户
    username: 用户名
    password: 密码
    mobile: 手机号
    email: 邮箱
    code: 验证码
    roles: 用户角色列表
    """

    # 步骤1: 接收并验证请求数据
    data = UserRegisterSchema().load(request.json)

    username = data['username']
    mobile = data['mobile']
    email = data['email']
    password = data['password']
    code = data['code']
    roles = data['roles']

    # 步骤2: 校验短信验证码
    #if not verify_sms_code(mobile, code, SMS_REDIS_REGISTER_PREFIX):
    if not code:
        return json_response(RET.PARAMERR, detailMsg="短信验证码错误")

    # 步骤3: 注册新用户
    try:
        user_service.register_user(username=username, email=email, mobile=mobile, password=password, roles=roles)
        return json_response(RET.OK)
    except Exception as e:
        current_app.logger.error(f"Error creating user: {e}")   
        return json_response(RET.DBSAVEERR, detailMsg="用户创建失败")
        
@api.route('/users/login/mobile', methods=['POST'])
@handle_api_call
def mobile_login():
    """
    通过手机验证码登录
    参数：
    mobile: 手机号
    code: 验证码
    device: 设备标识
    version: 设备版本
    """

    # 步骤1: 验证请求数据
    schema = MobileLoginSchema()
    data = schema.load(request.json)
    mobile = data.get('mobile')
    code = data.get('code')
    device = data.get('device')
    version = data.get('version')

    # 步骤2: 校验手机号用户是否是已激活注册用户
    user = user_service.validate_mobile(mobile)
    if not user:
        return json_response(RET.PARAMERR, detailMsg="手机号错误")

    # 步骤3: 校验短信验证码
    # if not verify_sms_code(mobile, code, SMS_REDIS_LOGIN_PREFIX):
    #     return json_response(RET.PARAMERR, detailMsg="短信验证码错误")
    if not code:
        return json_response(RET.PARAMERR, detailMsg="短信验证码错误")
    
    # 步骤4: 更新登录数据
    try:
        login_data = user_service.update_user_login_info(user, device, version)
        return json_response(RET.OK, data=login_data)
    except Exception as e:
        current_app.logger.error(f"Error updating user login info: {e}")
        return json_response(RET.SERVERERR, detailMsg="更新用户登录信息失败")
    
@api.route('/users/login', methods=['POST'])
@handle_api_call
def account_login():
    """
    通过账号密码登录
    参数：
    account: 账号
    password: 密码
    device: 设备标识
    version: 设备版本
    """

    # 步骤1: 验证请求数据
    schema = AccountLoginSchema()
    data = schema.load(request.json)

    account_input = data['account']
    password = data['password']
    device = data.get('device')
    version = data.get('version')
    # 步骤2: 校验输入账号对应用户是否是已激活注册用户
    user = user_service.validate_account(account_input, password)
    if user is None:
        return json_response(code=RET.PARAMERR, detailMsg="账号或密码错误") 

    # 步骤3: 更新登录数据
    try:
        login_data = user_service.update_user_login_info(user, device, version)
        return json_response(code=RET.OK, data=login_data)
    except Exception as e:
        current_app.logger.error(f"Error updating user login info: {e}")
        return json_response(code=RET.SERVERERR, detailMsg="更新用户登录信息失败")

@api.route('/users/<int:user_id>', methods=['GET'])
@handle_api_call
@token_auth.login_required
def get_user(user_id):
    """
    获取指定用户的详细信息
    参数：
    user_id: 用户的唯一标识ID
    """
    if not user_id:
        return json_response(RET.PARAMERR, detailMsg="缺少用户ID")

    user = user_service.get_user_by_id(user_id)
    if not user:
        return json_response(RET.PARAMERR, detailMsg="用户不存在")

    # 如果用户存在，返回用户的详细信息
    return json_response(RET.OK, data=user.to_dict())

@api.route('/users/<int:user_id>', methods=['PUT'])
@handle_api_call
@token_auth.login_required
def update_user(user_id):
    """
    更新指定用户的信息。
    
    参数：
    user_id (int): 用户的唯一标识ID，通过URL路径传递。
    
    请求体参数（通过JSON传递）：
    - username (str): 用户名。
    - email (str): 用户的电子邮件地址。
    - avatar (str, optional): 用户头像的URL。
    - status (int, optional): 用户的状态码。

    注意：请求体中的参数应符合 UserUpdateSchema 的定义。

    返回：
    如果成功，返回更新后的用户信息。
    如果更新失败或用户不存在，返回相应的错误信息。
    """
    if not user_id:
        return json_response(RET.PARAMERR, detailMsg="缺少用户ID")

    schema = UserUpdateSchema()
    data = schema.load(request.json)

    try:
        user = user_service.update_user(user_id, data)
        return json_response(RET.OK, data=user.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error updating user: {e}")
        return json_response(RET.DBSAVEERR, detailMsg="用户信息更新失败")

@api.route('/users/<int:user_id>/change-password', methods=['POST'])
@handle_api_call
@token_auth.login_required
def change_password():
    """
    允许用户更改自己的密码
    参数：
    user_id: 用户的唯一标识ID
    """
    user_id = request.json.get('user_id')  # 假设前端发送用户ID来标识注销的用户
    if not user_id:
        return json_response(RET.PARAMERR, detailMsg="缺少用户ID")

    data = PasswordChangeSchema().load(request.json)  

    user = user_service.get_user_by_id(user_id)  
    if not user:
        return json_response(RET.PARAMERR, detailMsg="用户不存在或已被禁用")

    try:
        user_service.change_user_password(user, data['new_password'])
        return json_response(RET.OK)
    except Exception as e:
        current_app.logger.error(f"Error changing user password: {e}")
        return json_response(RET.DBSAVEERR, detailMsg="密码更新失败")

@api.route('/users/reset-password/mobile', methods=['POST'])
@handle_api_call
def reset_password_by_mobile():
    '''
    通过手机验证码重置密码
    参数：
    mobile
    code
    repassword 新密码
    '''

    # 步骤1: 验证请求数据
    schema = ResetPasswordSchema()
    data = schema.load(request.json)

    mobile = data['mobile']
    sms_code = data['code']
    repassword = data['repassword']

    # 步骤2: 校验短信验证码
    # if not verify_sms_code(mobile, sms_code, SMS_REDIS_FORGET_PREFIX):
    if not sms_code:
        return json_response(RET.PARAMERR, detailMsg="短信验证码错误")

    # 步骤3: 校验用户是否存在
    user = user_service.validate_mobile(mobile)
    if not user:
        return json_response(RET.PARAMERR, detailMsg="手机号错误")

    # 步骤4: 重设密码
    try:
        user_service.reset_password(user, repassword)
        return json_response(RET.OK, detailMsg='密码修改成功')
    except Exception as e:
        current_app.logger.error(f"Error reseting user password: {e}")
        return json_response(RET.DBSAVEERR, detailMsg="密码更新失败")

@api.route('/users/reset-password/email/request', methods=['POST'])
@handle_api_call
def request_reset_password_email():
    '''
    请求通过邮件重置密码
    参数：
    email: 用户的电子邮件地址
    '''

    # 步骤1: 验证请求数据
    schema = EmailSchema()
    data = schema.load(request.json)

    email = data['email']

    # 步骤2: 校验邮箱用户是否是已激活注册用户
    user = user_service.validate_email(email)
    if user is None:
        return json_response(code=RET.PARAMERR, detailMsg="邮箱错误")   

    # 步骤3: 生成重置密码令牌并发送邮件
    reset_token = user_service.send_password_reset_email(user)

    # 步骤4: 返回成功响应
    return json_response(code=RET.OK, data={'reset_token': reset_token})

@api.route('/users/reset-password/email', methods=['POST'])
@handle_api_call
def reset_password_by_email():
    '''
    通过电子邮件链接重置密码
    参数：
    reset_token: 用户的重置令牌
    repassword: 新密码
    '''

    # 步骤1: 验证请求数据
    schema = ResetPasswordByEmailSchema()
    data = schema.load(request.json)

    reset_token = data['reset_token']
    repassword = data['repassword']

    # 步骤2: 校验 token
    user = User.verify_reset_token(reset_token)
    if user is None:
        return json_response(RET.PARAMERR, detailMsg="链接已失效")

    # 步骤3: 重设密码
    if user_service.reset_password(user, repassword) < 0: 
        return json_response(RET.DBSAVEERR, detailMsg="密码更新失败")

    # 步骤4: 返回成功响应
    return json_response(RET.OK, detailMsg="密码修改成功")

@api.route('/users/logout', methods=['POST'])
@handle_api_call
@token_auth.login_required
def logout():
    """
    用户注销登录
    """
    user_id = request.json.get('user_id')  # 假设前端发送用户ID来标识注销的用户
    if not user_id:
        return json_response(RET.PARAMERR, detailMsg="缺少用户ID")

    user = user_service.get_user_by_id(user_id)
    if not user:
        return json_response(RET.DATAERR, detailMsg="用户不存在")

    # 这里需要实现具体的注销逻辑，比如使用户的会话或令牌失效
    # 假设有一个方法 invalidate_user_session 来处理会话失效
    try:
        user_service.invalidate_user_session(user)
        return json_response(RET.OK)
    except Exception as e:  
        current_app.logger.error(f"Error logging out user: {e}")
        return json_response(RET.SERVERERR, detailMsg="注销失败，无法终止用户会话")