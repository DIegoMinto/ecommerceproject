# controllers/product_controller.py
from flask import Blueprint, request, render_template, jsonify, current_app
from services.product_service import ProductService
from werkzeug.utils import secure_filename
import os

product_blueprint = Blueprint('product', __name__)

product_service = ProductService()

@product_blueprint.route('/products', methods=['GET'])
def get_products():
    return jsonify([product.to_dict() for product in product_service.get_products()])

@product_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.form
    imagen = request.files.get('imagen')

    if imagen:
        filename = secure_filename(imagen.filename)
        imagen_url = f"/static/imagenes/{filename}"
        imagen_path = os.path.join(current_app.root_path, 'static/imagenes', filename)
        imagen.save(imagen_path)
    else:
        imagen_url = '/static/imagenes/placeholder.jpg'  # Una imagen por defecto

    product = product_service.create_product(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        precio=data['precio'],
        stock=data['stock'],
        imagen_url=imagen_url,
        categoria_id=data['categoria_id'],
        marca=data['marca'],
        modelo=data['modelo'],
        especificaciones=data['especificaciones']
    )
    return jsonify(product.to_dict()), 201


@product_blueprint.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = product_service.get_product(id)
    if product:
        return render_template('producto_detalle.html', producto=product)
    else:
        return jsonify({"message": "Producto no encontrado"}), 404

@product_blueprint.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = product_service.update_product(id, data['nombre'], data['descripcion'], data['precio'], data['stock'], data['imagen_url'], data['categoria_id'], data['marca'], data['modelo'], data['especificaciones'])
    return jsonify(product.to_dict()), 200

@product_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    return product_service.delete_product(id)
