# models/category.py
from extensions import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Define la relación inversa
    productos = db.relationship('Producto', back_populates='categoria')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
