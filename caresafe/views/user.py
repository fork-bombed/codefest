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


@bp.route('/extend', methods=['POST'])
@require_auth
def extend_session(user_id):

    try:
        data = request.get_json()
        extension = data.get('extension_time')
        appointment_id = data.get('appointment_id')

        user = User.query.get(user_id)
        appointment = Appointment.query.get(appointment_id)

        if user is None:
            return jsonify({'message': 'User not found'}), 404

        if appointment is None:
            return jsonify({'message': 'Appointment not found'}), 404

        if user.id != appointment.client_id:
            return jsonify({'message': 'Permission denied'}), 403

        appointment.duration += int(extension)
        db.session.commit()  # Commit changes to the database

        return jsonify({'message': 'Appointment extended'}), 200

    except (ValueError, IntegrityError) as e:
        db.session.rollback()  # Roll back changes on error
        return jsonify({'message': 'Invalid data or database error'}), 400

    except Exception as e:
        db.session.rollback()  # Roll back changes on error
        return jsonify({'message': f'Failed to update: {str(e)}'}), 400
