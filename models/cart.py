from extensions import db
from models.product import Producto

class Carrito(db.Model):
    __tablename__ = 'carritos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='carrito', uselist=False)
    
    # Relación con la tabla intermedia 'CarritoProducto'
    productos = db.relationship('CarritoProducto', backref='carrito', lazy=True)

    def get_productos(self):
        return [carrito_producto.producto for carrito_producto in self.productos]

class CarritoProducto(db.Model):
    __tablename__ = 'carrito_productos'
    id = db.Column(db.Integer, primary_key=True)
    carrito_id = db.Column(db.Integer, db.ForeignKey('carritos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    # Relación con Producto
    producto = db.relationship('Producto', backref='carrito_productos', lazy=True)
