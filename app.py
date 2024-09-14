from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Category, User, Producto
from flask import send_from_directory
from flask import render_template
import os
from werkzeug.utils import secure_filename



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
    
# Ruta para crear un producto y subir imágenes
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    # Verifica si la solicitud tiene archivos
    if 'imagen' not in request.files:
        return jsonify({"message": "No se ha proporcionado una imagen"}), 400

    imagen = request.files['imagen']
    if imagen.filename == '':
        return jsonify({"message": "No se seleccionó ninguna imagen"}), 400

    if imagen:
        # Genera un nombre único para la imagen
        imagen_filename = secure_filename(imagen.filename)
        imagen_path = os.path.join('static', 'imagenes', imagen_filename)
        imagen.save(imagen_path)
        
        # Construye la URL de la imagen para almacenar en la base de datos
        imagen_url = f"/static/imagenes/{imagen_filename}"

        # Obtén otros datos del formulario
        data = request.form
        nuevo_producto = Producto(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            precio=float(data['precio']),
            stock=int(data['stock']),
            imagen_url=imagen_url,
            categoria_id=int(data['categoria_id']),
            marca=data['marca'],
            modelo=data.get('modelo'),
            especificaciones=data.get('especificaciones')
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({"message": "Producto creado exitosamente"}), 201

# Ruta para obtener un producto
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([{
        "id": producto.id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": producto.precio,
        "stock": producto.stock,
        "imagen_url": producto.imagen_url,
        "categoria_id": producto.categoria_id,
        "marca": producto.marca,
        "modelo": producto.modelo,
        "especificaciones": producto.especificaciones,
        "fecha_creacion": producto.fecha_creacion
    } for producto in productos]), 200
    
# Ruta para eliminar un producto por ID
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get(id)
    
    if not producto:
        return jsonify({"message": "Producto no encontrado"}), 404
    
    db.session.delete(producto)
    db.session.commit()
    
    return jsonify({"message": "Producto eliminado exitosamente"}), 200
# Ruta para actualizar un producto por ID
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.get_json()
    producto = Producto.query.get(id)
    
    if not producto:
        return jsonify({"message": "Producto no encontrado"}), 404
    
    if 'nombre' in data:
        producto.nombre = data['nombre']
    if 'descripcion' in data:
        producto.descripcion = data.get('descripcion')
    if 'precio' in data:
        producto.precio = data['precio']
    if 'stock' in data:
        producto.stock = data['stock']
    if 'imagen_url' in data:
        producto.imagen_url = data['imagen_url']
    if 'categoria_id' in data:
        categoria = Category.query.get(data['categoria_id'])
        if not categoria:
            return jsonify({"message": "Categoría no encontrada"}), 404
        producto.categoria_id = data['categoria_id']
    if 'marca' in data:
        producto.marca = data['marca']
    if 'modelo' in data:
        producto.modelo = data.get('modelo')
    if 'especificaciones' in data:
        producto.especificaciones = data.get('especificaciones')

    db.session.commit()
    
    return jsonify({"message": "Producto actualizado exitosamente"}), 200

# Ruta para la interfaz del login 
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para mostrar el formulario de crear productos
@app.route('/crear_producto', methods=['GET'])
def crear_producto_form():
    categorias = Category.query.all()  # Obtener todas las categorías
    return render_template('crear_producto.html', categorias=categorias)

# Ruta para mostrar un producto en navegador 
@app.route('/productos/<int:id>', methods=['GET'])
def mostrar_producto(id):
    producto = Producto.query.get(id)
    if producto is None:
        return jsonify({"message": "Producto no encontrado"}), 404
    return render_template('producto_detalle.html', producto=producto)


# Inicializar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
