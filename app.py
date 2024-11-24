# app.py
from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, session, url_for
from flask_cors import CORS
from extensions import db, migrate
from controllers.category_controller import category_blueprint
from controllers.product_controller import product_blueprint
from controllers.user_controller import user_blueprint
from controllers.cart_controller import cart_blueprint  # Agrega esta línea para el carrito
from services.carrito_service import CarritoService  # Importa el servicio de carrito
from services.product_service import ProductService  # Importa el servicio de productos
from models.product import Producto
from models.category import Category

import os

app = Flask(__name__, static_url_path='/static')
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.secret_key ='1234'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Definir la carpeta de archivos estáticos
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'imagenes')
app.static_folder = 'static'

# Asociar la base de datos con la app
db.init_app(app)
migrate.init_app(app, db)

# Registrar Blueprints
app.register_blueprint(category_blueprint, url_prefix='/api')
app.register_blueprint(product_blueprint, url_prefix='/api')
app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(cart_blueprint, url_prefix='/api')  # Registra el blueprint del carrito

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

def update_image_urls():
    with app.app_context():
        productos = Producto.query.all()
        for producto in productos:
            if producto.imagen_url:
                if not producto.imagen_url.startswith('/static/'):
                    if producto.imagen_url.startswith('imagenes/'):
                        producto.imagen_url = f"/static/{producto.imagen_url}"
                    else:
                        producto.imagen_url = f"/static/imagenes/{producto.imagen_url}"
        db.session.commit()
    print("URLs de imágenes actualizadas.")

# Rutas para servir archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Rutas para la interfaz de usuario
@app.route('/')
@app.route('/index.html')
def lista_productos():
    productos = ProductService.get_all_products()
    categorias = Category.query.all()
    username = session.get('username')  # Obtener el nombre del usuario logueado
    return render_template('index.html', productos=productos, categorias=categorias, username=username)
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/crear_producto', methods=['GET'])
def crear_producto_form():
    categorias = Category.query.all()
    return render_template('crear_producto.html', categorias=categorias)

@app.route('/producto/<int:id>')
def producto_detalle(id):
    producto = ProductService.get_product_by_id(id)  # Usamos el servicio para obtener el producto
    return render_template('producto_detalle.html', producto=producto)

@app.route('/producto/editar/<int:id>', methods=['GET'])
def editar_producto_form(id):
    producto = ProductService.get_product_by_id(id)  # Usamos el servicio para obtener el producto
    categorias = Category.query.all()
    return render_template('editar_producto.html', producto=producto, categorias=categorias)

@app.route('/producto/editar/<int:id>', methods=['POST'])
def editar_producto(id):
    # Actualizamos los datos del producto usando el servicio
    ProductService.update_product(id, request.form, request.files)
    return redirect(url_for('producto_detalle', id=id))

@app.route('/categoria/<int:id>')
def categoria_productos(id):
    categoria = Category.query.get_or_404(id)
    productos = ProductService.get_products_by_category(id)  # Usamos el servicio para obtener los productos de una categoría
    return render_template('categoria_productos.html', categoria=categoria, productos=productos)

# Rutas API para manejar el carrito
@app.route('/api/carrito/<int:id>', methods=['GET'])
def get_cart(id):
    carrito = CarritoService.get_carrito_by_id(id)  # Usamos el servicio de carrito
    if carrito:
        productos = carrito.get_productos()  # Accede a los productos asociados
        return jsonify([producto.to_dict() for producto in productos])
    else:
        return jsonify({'message': 'Carrito no encontrado'}), 404

@app.route('/api/carrito/<int:id>/comprar', methods=['DELETE'])
def comprar_carrito(id):
    try:
        # Llama al servicio para completar la compra y eliminar los productos o el carrito
        CarritoService.complete_purchase_and_delete_all(id)
        return jsonify({'message': 'Compra realizada y carrito eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

if __name__ == '__main__':
    update_image_urls()  # Actualizar URLs de imágenes al iniciar la aplicación
    app.run(debug=True)
