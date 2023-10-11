from flask import Blueprint, jsonify
from caresafe.services.auth_service import require_auth

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@require_auth
def admin_home():
    return jsonify({'message': 'Welcome to the admin page!'})

# You can add more views to the admin blueprint here
