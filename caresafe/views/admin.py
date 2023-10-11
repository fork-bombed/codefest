from caresafe.models.models import Panic
from flask import Blueprint, jsonify, request
from caresafe.services.auth_service import require_auth, require_admin
from caresafe.models.models import Appointment, Client

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


@bp.route('/appointments', methods=['POST'])
@require_auth
@require_admin
def create_appointment(user_id):
    data = request.get_json()
    time = data.get('time')
    duration = data.get('duration')
    client_id = data.get('client_id')
    target_user_id = data.get('user_id')
    appointment = Appointment(time=time, duration=duration, client_id=client_id, user_id=target_user_id)
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
                    'time': appointment.time.strftime('%H:%M'),
                    'duration': appointment.duration,
                    'client_id': appointment.client_id,
                    'user_id': appointment.user_id,
                }
                for appointment in appointments
            ]
        }
    )


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
