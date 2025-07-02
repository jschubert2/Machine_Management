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
        "firstname": user.firstname,
        "lastname": user.lastname,
        "created_at": user.created_at.strftime('%Y-%m-%d')
    } for user in users]

    return jsonify(data)

@bp.route('/user', methods=['POST'])
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
    try:
        user = User(
            username=data['username'],
            firstname=data['first_name'],
            lastname=data['last_name'],
            created_at=datetime.utcnow().strftime("%Y-%m-%d")
        )

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "New user added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500