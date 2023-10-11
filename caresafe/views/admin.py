from flask import Blueprint, jsonify, request
from caresafe.services.auth_service import require_auth, require_admin
from caresafe.models.models import Appointment, Client, Panic

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


@bp.route('/appointments', methods=['POST'])
@require_auth
@require_admin
def create_appointment(user_id):
    data = request.get_json()
    date = data.get('date')
    duration = data.get('duration')
    client_id = data.get('client_id')
    target_user_id = data.get('user_id')
    appointment = Appointment(duration=duration, client_id=client_id, user_id=target_user_id)
    appointment.set_status("active")
    appointment.set_date(date)
    appointment.save()
    return jsonify({'message': 'Appointment created', 'id': appointment.id}), 201


@bp.route('/appointments', methods=['GET'])
@require_auth
@require_admin
def get_appointments(user_id):
    appointments = Appointment.query.all()
    return jsonify(
        {
            'appointments': [
                {
                    'id': appointment.id,
                    'date': appointment.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': appointment.duration,
                    'client': appointment.client.as_dict(),
                    'user': appointment.user.as_dict(),
                }
                for appointment in appointments
            ]
        }
    )


@bp.route('/appointments/<appointment_id>/decline', methods=['POST'])
@require_auth
@require_admin
def decline_appointment(user_id, appointment_id):
    to_status = 'declined'
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': f'Appointment with ID {appointment_id} was not found.'}), 404

    appointment.set_status(to_status)
    appointment.save()
    return jsonify({'status': to_status})


@bp.route('/clients', methods=['POST'])
@require_auth
@require_admin
def create_client(user_id):
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')
    address = data.get('address')
    client = Client(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
    client.save()
    return jsonify({'message': 'Client created', 'id': client.id}), 201


@bp.route('/clients', methods=['GET'])
@require_auth
@require_admin
def get_clients(user_id):
    clients = Client.query.all()
    return jsonify(
        {
            'clients': [
                {
                    'id': client.id,
                    'first_name': client.first_name,
                    'last_name': client.last_name,
                    'phone_number': client.phone_number,
                    'address': client.address,
                }
                for client in clients
            ]
        }
    )
