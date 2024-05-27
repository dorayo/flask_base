from app.schemas.user_schemas import AdminUserRegisterSchema 
from . import admin
from flask import request, current_app
from app.utils.api_utils import json_response, RET, handle_api_call
from app.services import user_service
from app.services.auth_service import token_auth
from app.models.user import User
from app.utils.role_utils import require_admin_role

@admin.route('/users', methods=['GET'])
@token_auth.login_required
@require_admin_role
@handle_api_call
def list_users():
    """
    获取用户列表，包括分页和筛选功能。
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = user_service.get_users_paginated(page, per_page)
    return json_response(RET.OK, data={'users': [user.to_dict() for user in users]})

@admin.route('/add_user', methods=['POST'])
@token_auth.login_required
@require_admin_role
def add_user():
    # 步骤1: 接收并验证请求数据
    data = AdminUserRegisterSchema().load(request.json)

    username = data['username']
    mobile = data['mobile']
    email = data['email']
    password = data['password']
    roles = data['roles']

    # 步骤2: 创建用户，暂时复用 register_user 方法
    try:
        user_service.register_user(username=username, email=email, mobile=mobile, password=password, roles=roles)
        return json_response(RET.OK)
    except Exception as e:
        current_app.logger.error(f"Error creating user: {e}")
        return json_response(RET.DBSAVEERR, detailMsg="用户创建失败")

@admin.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required
@require_admin_role
@handle_api_call
def update_user(user_id):
    """
    更新指定用户的信息，如状态等。
    """
    user_data = request.json
    try:
        user = user_service.update_user(user_id, user_data)
        return json_response(RET.OK, data=user.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error updating user: {e}")
        return json_response(RET.DBSAVEERR, detailMsg="用户信息更新失败")

@admin.route('/users/<int:user_id>/roles', methods=['POST'])
@token_auth.login_required
@require_admin_role
@handle_api_call
def add_user_role(user_id):
    """
    为用户添加角色。
    """
    data = request.json
    role_name = data.get('role_name')
    if not role_name:
        return json_response(RET.PARAMERR, detailMsg="缺少角色名称")

    try:
        user_service.add_role_to_user(user_id, role_name)
        return json_response(RET.OK, detailMsg="角色已添加")
    except Exception as e:
        current_app.logger.error(f"Error adding role to user: {e}")
        return json_response(RET.DBSAVEERR, detailMsg="添加角色失败")

@admin.route('/users/<int:user_id>/roles', methods=['DELETE'])
@token_auth.login_required
@require_admin_role
@handle_api_call
def remove_user_role(user_id):
    """
    为用户删除角色。
    """
    data = request.json
    role_name = data.get('role_name')
    if not role_name:
        return json_response(RET.PARAMERR, detailMsg="缺少角色名称")

    try:
        user_service.remove_role_from_user(user_id, role_name)
        return json_response(RET.OK, detailMsg="角色已删除")
    except Exception as e:
        current_app.logger.error(f"Error removing role from user: {e}")
        return json_response(RET.DBSAVEERR, detailMsg="删除角色失败")

@admin.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required
@require_admin_role
@handle_api_call
def delete_user(user_id):
    """
    删除用户，通常是标记用户为禁用状态。
    """
    try:
        user_service.deactivate_user(user_id)
        return json_response(RET.OK, detailMsg="用户已删除")
    except Exception as e:
        current_app.logger.error(f"Error deleting user: {e}")
        return json_response(RET.DBSAVEERR, detailMsg="用户删除失败")

@admin.route('/users/<int:user_id>', methods=['GET'])
@token_auth.login_required
@require_admin_role
@handle_api_call
def get_user(user_id):
    """
    获取单个用户的详细信息。
    """
    try:
        user = user_service.get_user_by_id(user_id)
        return json_response(RET.OK, data=user.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error getting user: {e}")
        return json_response(RET.DBERR, detailMsg="获取用户信息失败")
