import jwt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify, current_app
from werkzeug.security import check_password_hash
from models import User
# from app import app, db
from application.database import db
from sqlalchemy.orm import Session

# SECRET_KEY = app.config['SECRET_KEY']

def login():
    with Session(db.engine) as session:
        with session.begin():
            auth_data = request.json

            if not auth_data or not auth_data.get('username') or not auth_data.get('password'):
                return jsonify({'message': 'Missing credentials'}), 400

            user = session.query(User).filter_by(username=auth_data['username']).first()

            if user and check_password_hash(user.password, auth_data['password']):
                # Use current_app to access the SECRET_KEY
                SECRET_KEY = current_app.config['SECRET_KEY']

                # Create a token with an expiration of 30 minutes
                token = jwt.encode(
                    {
                        'username': user.username,
                        'role': user.role.name,  # Assuming the User model has a related 'role' attribute
                        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
                    },
                    SECRET_KEY,
                    algorithm="HS256"
                )
                return jsonify({'token': token}), 200

            return jsonify({'message': 'Invalid credentials'}), 401
