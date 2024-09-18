from flask import Blueprint, request, jsonify
from extensions import db
from services.user_service import UserService

user_blueprint = Blueprint('user', __name__)

user_service = UserService()

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    return jsonify([user.to_dict() for user in user_service.get_users()])

@user_blueprint.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    user = user_service.register_user(data['username'], data['email'], data['password'], data['rol'])
    return jsonify(user.to_dict()), 201

@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    return user_service.login_user(data['username'], data['password'])