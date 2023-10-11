from flask import Blueprint, jsonify, request
from caresafe.models.models import User
from caresafe import bcrypt
from caresafe.definitions import SECRET_KEY
from caresafe.services.auth_service import require_auth, generate_token


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
def auth_home():
    return jsonify({'message': 'Welcome to the auth page!'})

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username:
        return jsonify({'message': 'Username is required'}), 400
    if not password:
        return jsonify({'message': 'Password is required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    if len(username) < 3:
        return jsonify({'message': 'Username must be at least 3 characters'}), 400
    new_user = User(username=username, password=password)
    new_user.set_password(password)
    new_user.save()
    return jsonify({'message': 'User registered'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 401
    
    if bcrypt.check_password_hash(user.password, password):
        token = generate_token(user)
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@bp.route('/refresh', methods=['POST'])
@require_auth
def refresh_auth(user_id):
    user = User.query.get(user_id)
    token = generate_token(user)
    return jsonify({'token': token}), 200