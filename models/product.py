# models/product.py
from extensions import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    marca = db.Column(db.String(100), nullable=True)
    modelo = db.Column(db.String(100), nullable=True)
    especificaciones = db.Column(db.Text, nullable=True)

    # Define la relación
    categoria = db.relationship('Category', back_populates='productos')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'imagen_url': self.imagen_url,
            'categoria_id': self.categoria_id,
            'categoria': self.categoria.to_dict() if self.categoria else None,
            'marca': self.marca,
            'modelo': self.modelo,
            'especificaciones': self.especificaciones
        }
