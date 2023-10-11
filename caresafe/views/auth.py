from flask import Blueprint, jsonify

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/')
def auth_home():
    return jsonify({'message': 'Welcome to the auth page!'})
