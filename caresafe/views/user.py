from flask import Blueprint, jsonify, request
from caresafe.services.auth_service import require_auth
from caresafe.models.models import User, Panic, Appointment
from sqlalchemy.exc import IntegrityError
from caresafe import db


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


@bp.route('/checkin', methods=['POST'])
@require_auth
def check_in(user_id):
    user = User.query.get(user_id)
    user.checked_in = True
    user.save()
    return jsonify({'check in status': user.checked_in})


@bp.route('/checkout', methods=['POST'])
@require_auth
def check_out(user_id):
    user = User.query.get(user_id)
    user.checked_in = False
    user.save()
    return jsonify({'check in status': user.checked_in})


@bp.route('/<int:user_id>/appointments', methods=['GET'])
def get_user_appointments_by_id(user_id):
    user = User.query.get_or_404(user_id)
    appointments = user.appointments

    appointment_list = [{'id': appt.id, 'date': appt.date} for appt in appointments]
    return jsonify(appointment_list)


@bp.route('/<int:user_id>/appointments/<int:appt_id>', methods=['GET'])
def get_user_appointment_by_appt_id(user_id, appt_id):
    appt = Appointment.query.get_or_404(appt_id)

    return jsonify({'selected appointment': appt.as_dict()})

