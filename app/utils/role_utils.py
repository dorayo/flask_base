from functools import wraps
from flask import request, g
from app.utils.api_utils import json_response, RET
from app.services.auth_service import token_auth

# 角色到权限的映射
ROLE_PERMISSIONS = {
    'Admin': {'manage_users', 'view_any_data', 'edit_any_data', 'view_sensitive_data'},
    'Editor': {'edit_own_data', 'view_any_data'},
    'Viewer': {'view_any_data'},
    'User': {'view_own_data'}
}

def check_permissions(permission):
    """
    装饰器工厂，根据提供的权限字符串生成装饰器，检查用户是否有相应的权限。
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = token_auth.current_user().role
            allowed_permissions = ROLE_PERMISSIONS.get(user_role, set())
            if permission in allowed_permissions:
                return f(*args, **kwargs)
            else:
                return json_response(RET.AUTHERR, detailMsg="权限不足")
        return decorated_function
    return decorator

def require_role(role):
    """
    装饰器，要求用户必须具有指定的角色。
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if token_auth.current_user().role != role:
                return json_response(RET.AUTHERR, detailMsg="角色不符合要求")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming the token_auth has already verified the user and stored it in g.user
        user = token_auth.current_user()
        
        # Using Python's any() function for a more concise and efficient check
        if any(role.role_name == 'Admin' for role in user.roles):
            return f(*args, **kwargs)
        
        # Return an error if the user does not have the Admin role
        return json_response(RET.AUTHERR, detailMsg="Access denied: Admin role required.")

    return decorated_function