import jwt
from functools import wraps
from flask import request, jsonify, current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        SECRET_KEY = current_app.config['SECRET_KEY']
        token = None

        # Get the token from the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Decode token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_data = data  # Attach user data to the request context
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        SECRET_KEY = current_app.config['SECRET_KEY']
        token = None

        # Get the token from the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Decode token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data.get('role') != 'administrator':
                return jsonify({'message': 'Administrator role required'}), 403
            request.user_data = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated
