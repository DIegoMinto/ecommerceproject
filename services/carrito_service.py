from models.cart import Carrito, CarritoProducto
from models.product import Producto
from extensions import db
from repositories.carrito_repository import CarritoRepository

class CarritoService:

    @staticmethod
    def get_cart(user_id):
        carrito = CarritoRepository.get_cart_by_user_id(user_id)
        if not carrito:
            raise ValueError('Carrito no encontrado')
        
        productos = [
            {
                'producto_id': item.producto_id,
                'nombre': item.producto.nombre,
                'cantidad': item.cantidad,
                'precio': item.producto.precio,
            }
            for item in carrito.productos
        ]
        
        return {'carrito_id': carrito.id, 'productos': productos}

    @staticmethod
    def add_to_cart(user_id, producto_id, cantidad=1):
        carrito = CarritoRepository.get_cart_by_user_id(user_id)
        if not carrito:
            carrito = Carrito(user_id=user_id)
            CarritoRepository.add_carrito(carrito)

        producto = Producto.query.get(producto_id)
        if not producto:
            raise ValueError('Producto no encontrado')

        item = CarritoRepository.get_item_in_cart(carrito.id, producto_id)
        if item:
            item.cantidad += cantidad
        else:
            item = CarritoProducto(carrito_id=carrito.id, producto_id=producto_id, cantidad=cantidad)
            CarritoRepository.add_item_to_cart(item)

        return {'message': 'Producto añadido al carrito'}

    @staticmethod
    def remove_from_cart(user_id, producto_id):
        carrito = CarritoRepository.get_cart_by_user_id(user_id)
        if not carrito:
            raise ValueError('Carrito no encontrado')

        item = CarritoRepository.get_item_in_cart(carrito.id, producto_id)
        if not item:
            raise ValueError('Producto no encontrado en el carrito')

        CarritoRepository.remove_item_from_cart(item)
        return {'message': 'Producto eliminado del carrito'}

    @staticmethod
    def complete_purchase_and_delete_products(carrito_id):
        CarritoRepository.delete_all_items_in_cart(carrito_id)
        return {'message': 'Productos del carrito eliminados exitosamente'}

    @staticmethod
    def complete_purchase_and_delete_all(carrito_id):
        CarritoRepository.delete_all_items_in_cart(carrito_id)
        carrito = Carrito.query.get(carrito_id)
        if carrito:
            CarritoRepository.delete_carrito(carrito)
        return {'message': 'Compra realizada y carrito eliminado exitosamente'}
