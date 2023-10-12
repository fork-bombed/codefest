from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlite3 import IntegrityError


from caresafe import db, scheduler
from caresafe.services.auth_service import require_auth
from caresafe.models.models import User, Panic, Appointment
from sqlalchemy.exc import IntegrityError
import uuid


bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('', methods=['GET'])
@require_auth
def user_home(user_id):
    user = User.query.get(user_id)
    return jsonify(user.as_dict()), 200


@bp.route('/appointments/<int:appt_id>/panic', methods=['POST'])
@require_auth
def user_panic(user_id, appt_id):
    panic = Panic(appointment_id=appt_id, user_id=user_id)
    panic.save()
    return jsonify({'message': 'Panic created', 'id': panic.id}), 201


@bp.route('/call_admin', methods=['GET'])
def call_admin():
    phone = "07733891033"
    return jsonify({'phone': phone})


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


@bp.route('/appointments/<int:appt_id>/checkin', methods=['POST'])
@require_auth
def check_in(user_id, appt_id):
    user = User.query.get(user_id)
    user.checked_in = True
    user.check_in_ts = datetime.datetime.now()
    user.save()
    ten_min_check_in(user, appt_id)
    return jsonify({'check in status': user.checked_in}), 200


@bp.route('/appointments/<int:appt_id>/second-checkin', methods=['POST'])
@require_auth
def second_check_in(user_id):
    user = User.query.get(user_id)
    user.check_in_2 = True
    user.check_in_2_ts = datetime.datetime.now()
    user.save()
    return jsonify({'status': user.checked_in})


@bp.route('/appointments/<int:appt_id>/checkout', methods=['POST'])
@require_auth
def check_out(user_id):
    user = User.query.get(user_id)
    user.checked_in = False
    user.save()
    return jsonify({'status': user.checked_in})


@bp.route('/appointments/<int:appt_id>', methods=['GET'])
def get_user_appointments_by_id(appt_id):
    appt = Appointment.query.get_or_404(appt_id)

    return jsonify(appt.as_dict())


@bp.route('/appointments/<int:appointment_id>/decline', methods=['POST'])
@require_auth
def decline_appointment(user_id, appointment_id):
    to_status = 'declined'
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': f'Appointment with ID {appointment_id} was not found.'}), 404

    if user_id != appointment.user_id:
        return jsonify({'error': f'Appointment with ID {appointment_id} does not belong to user with ID {user_id}.'}), 403

    appointment.set_status(to_status)
    appointment.save()
    return jsonify({'status': to_status})


def second_check_in_checker(user, appt_id):
    if not user.check_in_2:
        delayed_panic(user, appt_id)


def ten_min_check_in(user, appt_id):
    job_id = str(uuid.uuid4())
    scheduler.add_job(func=second_check_in_checker, run_date=datetime.now() + timedelta(seconds=5),
                      args=[user, appt_id], id=job_id)


def call_panic_interm(user, appt_id):
    from caresafe import app
    panic = Panic(appointment_id=appt_id, user_id=user.id)
    with app.app_context():
        panic.save()


def delayed_panic(user, appt_id):
    job_id = str(uuid.uuid4())
    scheduler.add_job(func=call_panic_interm, run_date=datetime.now() + timedelta(seconds=5),
                      args=[user, appt_id], id=job_id)
