from flask import Blueprint, jsonify
from caresafe.services.auth_service import require_auth

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
@require_auth
def user_home(user_id):
    return jsonify({'message': f'Welcome to the user page {user_id}'})
