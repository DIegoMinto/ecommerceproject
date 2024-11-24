from flask import Blueprint, request, render_template, jsonify, current_app
from services.product_service import ProductService
from werkzeug.utils import secure_filename
import os

product_blueprint = Blueprint('product', __name__)

product_service = ProductService()

# Obtener todos los productos (API)
@product_blueprint.route('/products', methods=['GET'])
def get_products():
    try:
        products = product_service.get_products()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Crear un nuevo producto (API)
@product_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.form
    imagen = request.files.get('imagen')

    # Validación de entrada
    if not data.get('nombre') or not data.get('precio'):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    if imagen:
        filename = secure_filename(imagen.filename)
        imagen_url = f"/static/imagenes/{filename}"
        imagen_path = os.path.join(current_app.root_path, 'static/imagenes', filename)
        imagen.save(imagen_path)
    else:
        imagen_url = '/static/imagenes/placeholder.jpg'  # Imagen por defecto si no se sube una imagen

    try:
        product = product_service.create_product(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=data['precio'],
            stock=data.get('stock', 0),
            imagen_url=imagen_url,
            categoria_id=data['categoria_id'],
            marca=data.get('marca', ''),
            modelo=data.get('modelo', ''),
            especificaciones=data.get('especificaciones', '')
        )
        return jsonify(product.to_dict()), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Obtener un producto por ID (Interfaz de usuario)
@product_blueprint.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = product_service.get_product(id)
    if product:
        return render_template('producto_detalle.html', producto=product)
    else:
        return jsonify({"message": "Producto no encontrado"}), 404

# Actualizar un producto (API)
@product_blueprint.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()

    # Validación de datos
    if not data.get('nombre') or not data.get('precio'):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    try:
        product = product_service.update_product(
            id,
            data['nombre'],
            data['descripcion'],
            data['precio'],
            data['stock'],
            data['imagen_url'],
            data['categoria_id'],
            data['marca'],
            data['modelo'],
            data['especificaciones']
        )
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Eliminar un producto (API)
@product_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product_service.delete_product(id)
        return jsonify({"message": "Producto eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
