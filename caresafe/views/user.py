from flask import Blueprint, jsonify

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def user_home():
    return jsonify({'message': 'Welcome to the user page!'})

# You can add more views to the admin blueprint here
