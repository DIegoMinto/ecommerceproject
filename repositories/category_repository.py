from models.category import Category
from extensions import db
from flask import jsonify


class CategoryRepository:
    def create_category(self, name, description):
        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        db.session.commit()
        return new_category

    def get_categories(self):
        return Category.query.all()

    def search_categories(self, name_query):
        return Category.query.filter(Category.name.ilike(f'%{name_query}%')).all()

    def delete_category(self, id):
        category = Category.query.get(id)
        if category is None:
            return jsonify({"message": "Category not found"}), 404
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200

    def update_category(self, id, name, description):
        category = Category.query.get(id)
        if not category:
            return jsonify({"message": "Category not found"}), 404
        if 'name' in name:
            category.name = name
        if 'description' in description:
            category.description = description
        db.session.commit()
        return jsonify({"message": "Category updated successfully"}), 200