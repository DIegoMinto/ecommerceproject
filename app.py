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
from models.user import User  # Asegúrate de tener un modelo User para la autenticación
import os
from flask_session import Session

app = Flask(__name__, static_url_path='/static')
CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app, supports_credentials=True)

app.secret_key = '1234'  # Cambia este valor por algo más seguro en producción

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de la sesión
app.config['SESSION_TYPE'] = 'filesystem'  # Definir el tipo de sesión como 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')  # Directorio donde se almacenarán las sesiones
Session(app)  # Inicializa la sesión

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

# Actualización de URLs de imágenes
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

# Función para autenticar al usuario
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):  # Supongamos que tienes un método verify_password
        return user
    return None

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

@app.route('/api/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.before_request
def log_session():
    print("Session contents:", dict(session))

@app.route('/session-info')
def session_info():
    return jsonify(dict(session))

@app.route('/crear_producto', methods=['GET'])
def crear_producto_form():
    categorias = Category.query.all()
    return render_template('crear_producto.html', categorias=categorias)

@app.route('/producto/<int:id>')
def producto_detalle(id):
    producto = ProductService.get_product_by_id(id)
    username = session.get('username')  # Obtener el nombre de usuario logueado
    return render_template('producto_detalle.html', producto=producto, username=username)

@app.route('/producto/editar/<int:id>', methods=['GET'])
def editar_producto_form(id):
    producto = ProductService.get_product_by_id(id)
    categorias = Category.query.all()
    return render_template('editar_producto.html', producto=producto, categorias=categorias)

@app.route('/producto/editar/<int:id>', methods=['POST'])
def editar_producto(id):
    ProductService.update_product(id, request.form, request.files)
    return redirect(url_for('producto_detalle', id=id))

@app.route('/categoria/<int:id>')
def categoria_productos(id):
    categoria = Category.query.get_or_404(id)
    productos = ProductService.get_products_by_category(id)
    return render_template('categoria_productos.html', categoria=categoria, productos=productos)

# Rutas API para manejar el carrito
@app.route('/api/carrito/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    carrito = CarritoService.get_cart(user_id)
    if carrito:
        productos = carrito.get_productos()
        return jsonify([producto.to_dict() for producto in productos])
    else:
        return jsonify({'message': 'Carrito no encontrado'}), 404

@app.route('/user/create_account')
def create_account():
    return render_template('create_account.html')

@app.route('/api/carrito/<int:id>/comprar', methods=['DELETE'])
def comprar_carrito(id):
    try:
        CarritoService.complete_purchase_and_delete_all(id)
        return jsonify({'message': 'Compra realizada y carrito eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Rutas de autenticación
@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Autenticar usuario
    user = authenticate_user(username, password)

    if user:
        # Establece las variables de sesión
        session['username'] = username
        session['user_id'] = user.id
        print("Session updated:", session.get('username'))  # Depuración

        # Redirige a la página principal tras el inicio de sesión
        return redirect(url_for('lista_productos'))
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout_api():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    update_image_urls()
    app.run(debug=True)
