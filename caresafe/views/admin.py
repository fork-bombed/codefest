from flask import Blueprint, jsonify

from caresafe.models.models import Panic
from caresafe.services.auth_service import require_auth, require_admin

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@require_auth
@require_admin
def admin_home(user_id):
    return jsonify({'message': 'Welcome to the admin page!'})


@bp.route('/panic', methods=['GET'])
def get_panic():
    panics = Panic.query.all()
    return jsonify({'panics': panics})


@bp.route('/call_admin', methods=['GET'])
def call_admin():
    phone = "07733891033"
    return jsonify({'phone': phone})

