from repositories.user_repository import UserRepository
from models.user import User
from extensions import db

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_users(self):
        return self.repository.get_users()
    
    def login_user(self, username, password):
        return self.repository.login_user(username, password)
    
    def register_user(self, username, email, password, rol):
        # Llamar a la función de registro del repositorio
        user = self.repository.register_user(username, email, password, rol)
        
        # Verificar si el usuario fue creado correctamente
        if user:
            return {"message": "Usuario creado exitosamente", "user": user.to_dict()}, 201  # O la respuesta que prefieras
        else:
            # En caso de error, por ejemplo, si el usuario ya existe
            return {"message": "El usuario ya existe o ocurrió un error"}, 400
