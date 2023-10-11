from flask import Blueprint, jsonify

from caresafe.models.models import Panic
from caresafe.services.auth_service import require_auth, require_admin

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@require_auth
@require_admin
def admin_home():
    return jsonify({'message': 'Welcome to the admin page!'})


@bp.route('/panic', methods=['GET'])
def get_panic():
    panics = Panic.query.all()
    return jsonify({'panics': panics})