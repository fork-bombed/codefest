from flask import Blueprint, jsonify
from caresafe.services.auth_service import require_auth, require_admin

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@require_auth
@require_admin
def admin_home(user_id):
    return jsonify({'message': 'Welcome to the admin page!'})

