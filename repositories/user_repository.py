from models.user import User
from extensions import db
from flask import jsonify
from werkzeug.security import generate_password_hash

from werkzeug.security import check_password_hash

class UserRepository:
    def login_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # Verifica la contraseña con el hash
            return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username}}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401


class UserRepository:
    def get_users(self):
        return User.query.all()

    def register_user(self, username, email, password, rol):
        new_user = User(
            username=username,
            email=email,
            password=password,
            rol=rol
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def login_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return user  # Devuelve el objeto user
        else:
            return None  # Devuelve None si no se encuentra el usuario o las credenciales son incorrectas