from flask import Blueprint, jsonify, request
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime
from models import db

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              username:
                type: string
              role:
                type: string
              created_at:
                type: string
    """
    users = User.query.all()
    data = [{
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    } for user in users]

    return jsonify(data)

@bp.route('/users', methods=['POST'])
def register_user():
    """
    Register a new user
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "new_user"
            password:
              type: string
              example: "securepassword123"
            role:
              type: string
              example: "technician"
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User registered successfully!"
      400:
        description: Missing username or password
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username and password are required."
      409:
        description: Username already exists
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username already exists."
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'technician')  # default role

    print(f"\n\n\n\t\t\tReceived data: {data}\n\n\n")

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