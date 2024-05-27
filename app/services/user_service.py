# user_service.py
from flask import current_app 
from app import db
from sqlalchemy import or_
from app.models.user import User, UserLoginRecord, Role
from app.utils.email import send_email
from datetime import datetime
from app.utils.data_utils import dict_assignment_to_model

def register_user(*, username: str, email: str, mobile: str, password: str, roles: list) -> int:
    if is_user_registered(username, email, mobile):
        return False 
    
    user = User(username=username, email=email, mobile=mobile)
    user.set_password(password)
    _add_roles_to_user(user, roles) 
    db.session.add(user)
    db.session.commit()

def _add_roles_to_user(user, roles):
    for role_name in roles:
        role = db.session.query(Role).filter_by(role_name=role_name).first()
        if role is None:
            raise ValueError(f"角色 {role_name} 不存在")
        user.roles.append(role)

def add_role_to_user(user_id, role_name):
    role = db.session.query(Role).filter_by(role_name=role_name).first()    
    user = db.session.query(User).filter_by(id=user_id).first()
    if role and user:
        user.roles.append(role)
        db.session.commit()

def remove_role_from_user(user_id, role_name):
    role = db.session.query(Role).filter_by(role_name=role_name).first()    
    user = db.session.query(User).filter_by(id=user_id).first()
    if role and user:
        user.roles.remove(role)
        db.session.commit()

def is_user_registered(username, email, mobile):
    return db.session.query(User).filter(
        User.username == username,
        User.email == email,
        User.mobile == mobile
    ).first() is not None   

def validate_mobile(mobile):
    # if mobile is registered and active
    user = db.session.query(User).filter_by(mobile=mobile).first()
    if user and user.status:
        return user

def validate_account(account_input, password):
    # username、email、mobile 三者只要有一个匹配即可
    user = db.session.query(User).filter(
        or_(
            User.username == account_input,
            User.email == account_input,
            User.mobile == account_input
        )
    ).first()
    if user and user.status and user.check_password(password):
        return user

def validate_email(email):
    user = db.session.query(User).filter_by(email=email).first()
    if user and user.status:
      return user

def update_user_login_info(user, device, version):
    # 更新 token 和 last_login_time
    token = user.get_token(change=True)
    now = datetime.now()
    user.last_login_time = now
    db.session.add(user)
    # 更新 user_login_record 表
    record = UserLoginRecord(user_id=user.id, device=device, version=version, last_login_time=now)
    db.session.add(record)
    db.session.commit()

    data = user.to_dict()
    data['token'] = token
    return data

def update_user(user_id, updates):
    user = db.session.query(User).filter_by(id=user_id).first()
    user = dict_assignment_to_model(updates, user)   
    db.session.commit()
    return user

def change_user_password(user, new_password):
    # 设置新密码
    user.set_password(new_password)
    # 提交更改到数据库
    db.session.commit()

def send_password_reset_email(user):
    # 生成重置密码的令牌和链接
    reset_token = user.generate_reset_token()
    reset_url = current_app.config['PASSWORD_RESET_URL'] + '?token=' + reset_token
    
    send_email(user.email, '重置密码', 'reset', username=user.username, token=reset_token, url=reset_url)
    return reset_token

def reset_password(user, new_password):
    user.set_password(new_password) 
    db.session.commit()

def deactivate_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    user.status = 0
    db.session.commit()

def get_user_by_id(user_id):
    return db.session.query(User).filter_by(id=user_id).first()

def get_user_by_email(email):
    return db.session.query(User).filter_by(email=email).first()

def get_user_by_username(username):
    return db.session.query(User).filter_by(username=username).first()

def get_users_paginated(page, per_page):
    # 计算开始的记录位置
    offset = (page - 1) * per_page
    # 生成查询，添加分页条件
    return db.session.query(User).offset(offset).limit(per_page).all()

def invalidate_user_session(user):
    """
    使用户的登录会话失效
    Args:
        user (User): 需要注销的用户对象

    Returns:
        bool: 返回True表示会话已成功失效，False表示操作失败
    """
    # 示例逻辑，需要根据实际使用的会话管理方法来实现
    try:
        # 假设使用 Redis 存储会话，这里删除对应的会话键
        # redis_store.delete(f'user_session:{user.id}')
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to invalidate session for user {user.id}: {str(e)}")
        return False
    

