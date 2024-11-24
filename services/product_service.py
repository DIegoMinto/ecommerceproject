# services/product_service.py
from models.product import Producto
from extensions import db
import os

class ProductService:
    @staticmethod
    def get_all_products():
        return Producto.query.all()

    @staticmethod
    def get_product_by_id(id):
        return Producto.query.get_or_404(id)

    @staticmethod
    def get_products_by_category(category_id):
        return Producto.query.filter_by(categoria_id=category_id).all()

    @staticmethod
    def update_product(id, form_data, file_data):
        producto = Producto.query.get_or_404(id)

        # Actualizar los datos del producto
        producto.nombre = form_data['nombre']
        producto.precio = float(form_data['precio'])
        producto.stock = int(form_data['stock'])
        producto.descripcion = form_data['descripcion']
        producto.categoria_id = form_data['categoria_id']

        # Si se subió una nueva imagen
        if 'imagen' in file_data:
            imagen = file_data['imagen']
            if imagen.filename != '':
                imagen_path = os.path.join('static', 'imagenes', imagen.filename)
                imagen.save(imagen_path)
                producto.imagen_url = f"/static/imagenes/{imagen.filename}"
        
        db.session.commit()
