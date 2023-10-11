from functools import wraps
from flask import request, jsonify
from caresafe.definitions import SECRET_KEY
import jwt

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'message': 'Missing Authorization header'}), 401
        
        token = verify_token(auth_header)

        if not token:
            return jsonify({'message': 'Invalid Token'}), 401
        
        kwargs["user_id"] = token.get('user_id')
        
        return f(*args, **kwargs)
    return decorated


def verify_token(auth_header):
    if not auth_header:
        return False
    
    auth_token = auth_header.split(" ")[1]  # Assumes "Bearer <TOKEN>"
    
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        return payload

    except jwt.ExpiredSignatureError:
        return False  # Signature has expired
    except jwt.InvalidTokenError:
        return False  # Invalid token