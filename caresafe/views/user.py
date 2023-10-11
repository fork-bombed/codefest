from flask import Blueprint, jsonify, request

from caresafe import db
from caresafe.services.auth_service import require_auth
from caresafe.models.models import User, Panic, Appointment
from sqlalchemy.exc import IntegrityError

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


<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 526ed0b (Refucked and unfucked the stuff)
=======
>>>>>>> 40bed54 (Fix smol issue)
@bp.route('/panic', methods=['POST'])
@require_auth
def user_panic(user_id):
    appointment_id = request.json.get('appointment_id')
    panic = Panic(appointment_id=appointment_id, user_id=user_id)
    panic.save()
<<<<<<< HEAD
    

<<<<<<< HEAD
=======
 
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

        if user.id != appointment.user.id:
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
=======
>>>>>>> 40bed54 (Fix smol issue)
    

>>>>>>> 526ed0b (Refucked and unfucked the stuff)
@bp.route('/appointments', methods=['GET'])
@require_auth
def get_user_appointments(user_id):
    user = User.query.get(user_id)
    appointments = user.appointments
    return jsonify(
        {
            'appointments': [appointment.as_dict() for appointment in appointments]
        }
    )
