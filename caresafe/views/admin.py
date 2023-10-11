from flask import Blueprint, jsonify

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
def admin_home():
    return jsonify({'message': 'Welcome to the admin page!'})

# You can add more views to the admin blueprint here
