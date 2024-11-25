from flask import Blueprint, request, jsonify, session
from services.user_service import UserService

user_blueprint = Blueprint('user', __name__)

# Crear la instancia de UserService
user_service = UserService()

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    return jsonify([user.to_dict() for user in user_service.get_users()])

@user_blueprint.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    
    # Validar si los campos necesarios existen
    if 'username' not in data or 'email' not in data or 'password' not in data or 'rol' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Si los campos están presentes, registramos al usuario
    user = user_service.register_user(data['username'], data['email'], data['password'], data['rol'])
    return jsonify(user.to_dict()), 201

@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Llamar al servicio para intentar hacer login
    user = user_service.login_user(username, password)

    if user:
        session['user_id'] = user.id  # Ya no es un tuple, es un objeto user
        return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username}}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
