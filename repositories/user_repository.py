from models.user import User
from extensions import db

class UserRepository:
    def get_users(self):
        return User.query.all()

    def register_user(self, username, email, password, rol):
        # Verifica si ya existe un usuario con el mismo email o nombre de usuario
        existing_user = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
        if existing_user:
            return None  # El usuario ya existe, no se puede crear uno nuevo

        # Crear un nuevo usuario (sin hashear la contraseña)
        new_user = User(username=username, email=email, password=password, rol=rol)

        # Guardar el nuevo usuario en la base de datos
        db.session.add(new_user)
        db.session.commit()

        return new_user

    def login_user(self, username, password):
        # Buscar al usuario por su nombre de usuario
        user = User.query.filter_by(username=username).first()

        # Verificar si existe el usuario y si la contraseña coincide
        if user and user.password == password:  # Compara las contraseñas en texto claro
            return user  # Devuelve el usuario si las credenciales son correctas
        else:
            return None  # Devuelve None si las credenciales son incorrectas o el usuario no existe
