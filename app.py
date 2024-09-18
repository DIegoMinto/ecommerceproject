# app.py
from flask import Flask, render_template, jsonify
from extensions import db, migrate
from models.product import Producto
from models.user import User
from models.category import Category
from controllers.category_controller import category_blueprint
from controllers.product_controller import product_blueprint
from controllers.user_controller import user_blueprint
from flask import send_from_directory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define la carpeta de archivos estáticos
app.config['UPLOAD_FOLDER'] = 'static/imagenes'

@app.route('/static/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Asociar la base de datos con la app
db.init_app(app)
migrate.init_app(app, db)

# Registrando Blueprints
app.register_blueprint(category_blueprint, url_prefix='/api')
app.register_blueprint(product_blueprint, url_prefix='/api')
app.register_blueprint(user_blueprint, url_prefix='/api')

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Rutas para la interfaz de usuario
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/crear_producto', methods=['GET'])
def crear_producto_form():
    categorias = Category.query.all()  # Obtener todas las categorías
    return render_template('crear_producto.html', categorias=categorias)

# app.py
@app.route('/producto/<int:id>')
def producto_detalle(id):
    producto = {
        'id': id,
        'nombre': 'Laptop blanca',
        'descripcion': 'Laptop blanca con tecla color azul',
        'precio': 100.0,
        'stock': 5,
        'marca': 'HP',
        'modelo': 'Pavilion Gaming',
        'especificaciones': '8GB RAM, 256 GB almacenamiento',
        'imagen_url': '/static/imagenes/laptop1.png',
        'categoria': {'name': 'Computadoras'}
    }
    return render_template('producto_detalle.html', producto=producto)


if __name__ == '__main__':
    app.run(debug=True)
