from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Category, User 
from flask import send_from_directory
from flask import render_template



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Asociar la base de datos con la app
db.init_app(app)
# Configurar Flask-Migrate
migrate = Migrate(app, db)
# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('', filename)


# Ruta para crear categorías
@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'], description=data.get('description'))
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created successfully"}), 201


# Ruta para obtener categorías
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])


# Ruta para buscar categorías por nombre
@app.route('/api/categories/search', methods=['GET'])
def search_categories():
    name_query = request.args.get('name', '')  # Obtiene el parámetro de búsqueda 'name' de la URL
    categories = Category.query.filter(Category.name.ilike(f'%{name_query}%')).all()  # Búsqueda por nombre
    categories_list = [{"id": category.id, "name": category.name} for category in categories]
    return jsonify(categories_list)

# Ruta para eliminar una categoría por ID
@app.route('/api/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({"message": "Category not found"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200

# Ruta para actualizar una categoría por ID
@app.route('/api/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    category = Category.query.get(id)
    
    if not category:
        return jsonify({"message": "Category not found"}), 404
    
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    
    db.session.commit()
    
    return jsonify({"message": "Category updated successfully"}), 200

# Ruta para obtener todos los usuarios
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'rol': user.rol
    } for user in users])

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
 
# Ruta para la interfaz del login 
@app.route('/login')
def login():
    return render_template('login.html')

# Inicializar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
