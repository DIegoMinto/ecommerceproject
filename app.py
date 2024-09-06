from flask import Flask, request, jsonify
from models import db, Category, User 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Asociar la base de datos con la app
db.init_app(app)

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Ruta para crear categorías
@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created successfully"}), 201

# Ruta para obtener categorías
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_list = [{"id": category.id, "name": category.name} for category in categories]
    return jsonify(categories_list)

# Ruta para registrar un usuario
@app.route('/api/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],  # Contraseña sin hashing
        rol='user'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Ruta para el inicio de sesión del usuario
@app.route('/api/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username}}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# Inicializar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
