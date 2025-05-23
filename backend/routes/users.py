from flask import Blueprint, jsonify, request
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime
from models import db

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    data = [{
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    } for user in users]

    return jsonify(data)

# // This route is for registering a new user

@bp.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'technician')  # default role
    
    print(f"\n\n\n\t\t\tReceived data: {data}\n\n\n")
    
    # print(f"Registering user: {username}, Role: {role}")

    if not username or not password:
        return {"error": "Username and password are required."}, 400

    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists."}, 409

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role,
        created_at=datetime.now()
    )

    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered successfully!"}, 201