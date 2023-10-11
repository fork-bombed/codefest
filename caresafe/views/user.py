from flask import Blueprint, jsonify, request

from caresafe.services.auth_service import require_auth
from caresafe.models.models import User, Panic

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
@require_auth
def user_home(user_id):
    user = User.query.get(user_id)
    return jsonify(
        {
            'message': f'Welcome {user.username}!',
        }
    )


@bp.route('/panic', methods=['POST'])
@require_auth
def user_panic(user_id):
    appointment_id = request.json.get('appointment_id')
    panic = Panic(appointment_id=appointment_id, user_id=user_id)
    panic.save()
