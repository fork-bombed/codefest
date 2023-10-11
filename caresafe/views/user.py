from flask import Blueprint, jsonify
from caresafe.services.auth_service import require_auth
from caresafe.models.models import User

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
