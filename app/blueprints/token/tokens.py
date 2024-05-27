from . import token
from flask import current_app
from app import db
from app.services.auth_service import basic_auth, token_auth
from app.utils.api_utils import RET, json_response, handle_api_call

@token.route('/tokens', methods=['POST'])
@handle_api_call
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    try:
        db.session.commit()
        return json_response(RET.OK, data={'token': token})
    except Exception as e:
        current_app.logger.error(f"Error saving token: {e}")
        return json_response(RET.DBSAVEERR, detailMsg=str(e))

@token.route('/tokens', methods=['DELETE'])
@handle_api_call
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    try:
        db.session.commit()
        return json_response(RET.OK, detailMsg="Token revoked successfully")
    except Exception as e:
        current_app.logger.error(f"Error revoking token: {e}")
        return json_response(RET.DBSAVEERR, detailMsg=str(e))
    