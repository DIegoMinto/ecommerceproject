# app.py
from flask import Flask, render_template, jsonify, send_from_directory
from flask import request, redirect, url_for
from flask_cors import CORS
from extensions import db, migrate
from models.product import Producto
from models.user import User
from models.category import Category
from services.category_service import CategoryService
from controllers.category_controller import category_blueprint
from controllers.product_controller import product_blueprint
from controllers.user_controller import user_blueprint
import os

app = Flask(__name__, static_url_path='/static')
CORS(app, resources={r"/api/*": {"origins": "*"}})

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
    productos = Producto.query.all()
    categorias = Category.query.all()
    return render_template('index.html', productos=productos,categorias=categorias)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/crear_producto', methods=['GET'])
def crear_producto_form():
    categorias = Category.query.all()
    return render_template('crear_producto.html', categorias=categorias)

@app.route('/producto/<int:id>')
def producto_detalle(id):
    producto = Producto.query.get_or_404(id)
    return render_template('producto_detalle.html', producto=producto)

@app.route('/producto/editar/<int:id>', methods=['GET'])
def editar_producto_form(id):
    producto = Producto.query.get_or_404(id)
    categorias = Category.query.all()
    return render_template('editar_producto.html', producto=producto, categorias=categorias)

@app.route('/producto/editar/<int:id>', methods=['POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    
    # Actualizar los datos del producto
    producto.nombre = request.form['nombre']
    producto.precio = float(request.form['precio'])
    producto.stock = int(request.form['stock'])
    producto.descripcion = request.form['descripcion']
    producto.categoria_id = request.form['categoria_id']

    # Si se subió una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
            imagen.save(imagen_path)
            producto.imagen_url = f"/static/imagenes/{imagen.filename}"
    
    db.session.commit()
    
    return redirect(url_for('producto_detalle', id=producto.id))

@app.route('/categoria/<int:id>')
def categoria_productos(id):
    categoria = Category.query.get_or_404(id)
    productos = Producto.query.filter_by(categoria_id=id).all()
    return render_template('categoria_productos.html', categoria=categoria, productos=productos)


if __name__ == '__main__':
    update_image_urls()  # Actualizar URLs de imágenes al iniciar la aplicación
    app.run(debug=True)