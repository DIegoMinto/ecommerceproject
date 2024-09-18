from flask import Blueprint, request, jsonify
from extensions import db
from services.product_service import ProductService

product_blueprint = Blueprint('product', __name__)

product_service = ProductService()

@product_blueprint.route('/products', methods=['GET'])
def get_products():
    return jsonify([product.to_dict() for product in product_service.get_products()])

@product_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = product_service.create_product(data['nombre'], data['descripcion'], data['precio'], data['stock'], data['imagen_url'], data['categoria_id'], data['marca'], data['modelo'], data['especificaciones'])
    return jsonify(product.to_dict()), 201

@product_blueprint.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = product_service.get_products().filter_by(id=id).first()
    if product:
        return jsonify(product.to_dict())
    else:
        return jsonify({"message": "Product not found"}), 404

@product_blueprint.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = product_service.update_product(id, data['nombre'], data['descripcion'], data['precio'], data['stock'], data['imagen_url'], data['categoria_id'], data['marca'], data['modelo'], data['especificaciones'])
    return jsonify(product.to_dict()), 200

@product_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    return product_service.delete_product(id)