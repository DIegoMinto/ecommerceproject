from flask import Blueprint, flash, render_template, request, jsonify, session, url_for, redirect, g
from services.carrito_service import CarritoService

cart_blueprint = Blueprint('cart', __name__)

# Obtener el carrito de un usuario
@cart_blueprint.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        carrito = CarritoService.get_cart(user_id)
        return jsonify(carrito)
    except ValueError as e:
        return jsonify({'message': str(e)}), 404

# Agregar un producto al carrito
@cart_blueprint.route('/cart/<int:user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    try:
        data = request.json
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 1)

        result = CarritoService.add_to_cart(user_id, producto_id, cantidad)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'message': str(e)}), 404

# Eliminar un producto del carrito
@cart_blueprint.route('/cart/<int:user_id>/remove', methods=['POST'])
def remove_from_cart(user_id):
    try:
        data = request.json
        producto_id = data.get('producto_id')

        result = CarritoService.remove_from_cart(user_id, producto_id)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'message': str(e)}), 404

# Eliminar solo los productos del carrito después de la compra
@cart_blueprint.route('/api/carrito/<int:id>', methods=['DELETE'])
def delete_cart_products(id):
    try:
        result = CarritoService.complete_purchase_and_delete_products(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

# Eliminar todo el carrito y productos después de la compra
@cart_blueprint.route('/api/carrito/delete/<int:id>', methods=['DELETE'])
def delete_cart(id):
    try:
        result = CarritoService.complete_purchase_and_delete_all(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@cart_blueprint.before_request
def require_login():
    if not session.get('user_id'):
        return jsonify({"message": "Debe iniciar sesión para acceder al carrito"}), 401
    
@cart_blueprint.route('/carrito', methods=['GET'])
def ver_carrito():
    # Validar que el usuario esté logueado
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user_controller.login'))  # Redirige al login si no está logueado
    
    # Obtener los productos del carrito
    try:
        carrito = CarritoService.get_cart(user_id)
    except ValueError as e:
        carrito = {'productos': [], 'carrito_id': None}
        flash(str(e), 'error')

    # Renderizar plantilla del carrito
    return render_template('carrito.html', carrito=carrito)
