from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de categorías (simulación de una base de datos en memoria)
categories = []

# Ruta para obtener todas las categorías
@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)

# Ruta para crear una nueva categoría
@app.route('/api/categories', methods=['POST'])
def create_category():
    new_category = request.json  # Obtiene los datos en formato JSON
    categories.append(new_category)  # Añade la nueva categoría a la lista
    return jsonify(new_category), 201

# Ruta para eliminar una categoría por ID
@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id < len(categories):
        removed_category = categories.pop(category_id)
        return jsonify(removed_category), 200
    else:
        return jsonify({"error": "Category not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
