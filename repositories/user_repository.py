from models.user import User
from extensions import db
from flask import jsonify


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
            return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username}}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401