from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo de Categoría
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

# Crear las tablas
with app.app_context():
    db.create_all()

@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created successfully"}), 201

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_list = [{"id": category.id, "name": category.name} for category in categories]
    return jsonify(categories_list)

if __name__ == '__main__':
    app.run(debug=True)
