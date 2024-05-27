from enum import Enum
from flask import current_app, jsonify, make_response
from http import HTTPStatus
from functools import wraps
from marshmallow import ValidationError

class RET(Enum):
    OK = 1
    PARAMERR = 1001
    AUTHERR = 1101
    SESSIONERR = 1102
    DBERR = 1201
    DBSAVEERR = 1202
    THIRDERR = 1301
    DATAERR = 1401
    SERVERERR = 1901
    UNKOWNERR = 2000

error_map = {
    RET.OK: ('成功', HTTPStatus.OK),
    RET.PARAMERR: ('参数错误', HTTPStatus.BAD_REQUEST),
    RET.AUTHERR: ('认证错误', HTTPStatus.UNAUTHORIZED),
    RET.SESSIONERR: ('token不存在或已过期', HTTPStatus.UNAUTHORIZED),
    RET.DBERR: ('数据库执行错误', HTTPStatus.INTERNAL_SERVER_ERROR),
    RET.DBSAVEERR: ('数据库存储错误', HTTPStatus.INTERNAL_SERVER_ERROR),
    RET.THIRDERR: ('第三方系统错误', HTTPStatus.BAD_GATEWAY),
    RET.DATAERR: ('数据错误', HTTPStatus.UNPROCESSABLE_ENTITY),
    RET.SERVERERR: ('内部错误', HTTPStatus.INTERNAL_SERVER_ERROR),
    RET.UNKOWNERR: ('未知错误', HTTPStatus.INTERNAL_SERVER_ERROR),
}

def json_response(code=RET.OK, detailMsg=None, data=None, headers=None):
    """
    Generate a JSON response for API calls.

    :param code: Status code for the response, using RET enum.
    :param detailMsg: Detailed message for debugging in development mode.
    :param data: Data to be included in the response body.
    :param headers: Additional headers to be included in the response.
    """
    message, http_status = error_map.get(code, ('未知错误', HTTPStatus.INTERNAL_SERVER_ERROR))
    response_data = {
        'code': code.value,  # 使用 `.value` 获取枚举的基本值
        'message': message,
        'data': data or {}
    }

    # 根据当前环境决定是否添加detailMsg字段
    if current_app.config['DEBUG'] and detailMsg:
        response_data['detailMsg'] = detailMsg

    response = jsonify(response_data)
    response.status_code = http_status

    if http_status != HTTPStatus.OK:
        current_app.logger.error(f"Error {code}: {message} {detailMsg if detailMsg else ''}")

    # 设置跨域头信息
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'x-requested-with,content-type'
    })

    if headers:
        response.headers.update(headers)

    return response

def handle_api_call(func):
    """
    A decorator to handle exceptions and automate response generation for API calls.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            current_app.logger.debug(f'Validation error in {func.__name__}: {err.messages}')
            return json_response(code=RET.PARAMERR)
        except Exception as e:
            current_app.logger.error(f'Unhandled error in {func.__name__}: {str(e)}') 
            return json_response(code=RET.SERVERERR)
    return wrapper

