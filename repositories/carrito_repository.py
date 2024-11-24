from models.cart import Carrito, CarritoProducto
from models.product import Producto
from extensions import db

class CarritoRepository:

    @staticmethod
    def get_cart_by_user_id(user_id):
        return Carrito.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_item_in_cart(carrito_id, producto_id):
        return CarritoProducto.query.filter_by(carrito_id=carrito_id, producto_id=producto_id).first()

    @staticmethod
    def add_carrito(carrito):
        db.session.add(carrito)
        db.session.commit()

    @staticmethod
    def add_item_to_cart(item):
        db.session.add(item)
        db.session.commit()

    @staticmethod
    def remove_item_from_cart(item):
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def delete_all_items_in_cart(carrito_id):
        carrito = Carrito.query.get(carrito_id)
        if carrito:
            for item in carrito.productos:
                db.session.delete(item)
            db.session.commit()

    @staticmethod
    def delete_carrito(carrito):
        db.session.delete(carrito)
        db.session.commit()
