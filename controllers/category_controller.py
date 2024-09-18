from flask import Blueprint, request, jsonify
from extensions import db
from services.category_service import CategoryService

category_blueprint = Blueprint('category', __name__)

category_service = CategoryService()

@category_blueprint.route('/categories', methods=['GET'])
def get_categories():
    return jsonify([category.to_dict() for category in category_service.get_categories()])

@category_blueprint.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category = category_service.create_category(data['name'], data['description'])
    return jsonify(category.to_dict()), 201

@category_blueprint.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = category_service.get_categories().filter_by(id=id).first()
    if category:
        return jsonify(category.to_dict())
    else:
        return jsonify({"message": "Category not found"}), 404

@category_blueprint.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    category = category_service.update_category(id, data['name'], data['description'])
    return jsonify(category.to_dict()), 200

@category_blueprint.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    return category_service.delete_category(id)