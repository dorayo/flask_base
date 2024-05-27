# 图片验证码Redis有效期， 单位：秒
IMAGE_CODE_REDIS_EXPIRES = 120  

# 短信验证码Redis有效期，单位：秒
SMS_CODE_REDIS_EXPIRES = 300  

# 登录验证码redis前缀
SMS_REDIS_LOGIN_PREFIX = "sms_login_"

# 忘记密码验证码redis前缀
SMS_REDIS_FORGET_PREFIX = 'sms_forget_'

# 注册验证码redis前缀
SMS_REDIS_REGISTER_PREFIX = 'sms_register_'

# 默认每页条数
APP_NORMAL_LIST_PAGE_COUNT = 10

# token失效时间
ACTIVE_USER_BEFORE_DAY = 30

# 登录的最大错误次数
LOGIN_ERROR_MAX_NUM = 5  

# 登录错误封ip的时间，单位：秒
LOGIN_ERROR_FORBID_TIME = 600  

# 角色定义
ADMIN = "Admin"
EDITOR = "Editor"
VIEWER = "Viewer"
USER = "User"
ROLES_LIST = [ADMIN, EDITOR, VIEWER, USER]
ROLES = [
    {'role_name': ADMIN},
    {'role_name': EDITOR},
    {'role_name': VIEWER},
    {'role_name': USER},
]

# 权限定义
PERMISSIONS = [
    {'permission_name': 'view_own_data'},
    {'permission_name': 'view_any_data'},
    {'permission_name': 'view_sensitive_data'},
    {'permission_name': 'edit_own_data'},
    {'permission_name': 'edit_any_data'},
    {'permission_name': 'manage_users'},
]