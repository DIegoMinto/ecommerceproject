from models.product import Producto
from models.category import Category
from extensions import db
from flask import jsonify
from sqlalchemy.orm import joinedload


# repositories/product_repository.py
class ProductoRepository:
    def crear_producto(self, nombre, descripcion, precio, stock, imagen_url, categoria_id, marca, modelo, especificaciones):
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen_url=imagen_url,
            categoria_id=categoria_id,
            marca=marca,
            modelo=modelo,
            especificaciones=especificaciones
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return nuevo_producto

    def obtener_productos(self):
        return Producto.query.all()

    def obtener_producto_por_id(self, id):
        # Carga la relación `categoria` junto con el producto
        return Producto.query.options(joinedload(Producto.categoria)).get(id)

    def eliminar_producto(self, id):
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({"message": "Producto no encontrado"}), 404
        db.session.delete(producto)
        db.session.commit()
        return jsonify({"message": "Producto eliminado exitosamente"}), 200

    def actualizar_producto(self, id, nombre, descripcion, precio, stock, imagen_url, categoria_id, marca, modelo, especificaciones):
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({"message": "Producto no encontrado"}), 404
        if 'nombre' in nombre:
            producto.nombre = nombre
        if 'descripcion' in descripcion:
            producto.descripcion = descripcion
        if 'precio' in precio:
            producto.precio = precio
        if 'stock' in stock:
            producto.stock = stock
        if 'imagen_url' in imagen_url:
            producto.imagen_url = imagen_url
        if 'categoria_id' in categoria_id:
            categoria = Category.query.get(categoria_id)
            if not categoria:
                return jsonify({"message": "Categoría no encontrada"}), 404
            producto.categoria_id = categoria_id
        if 'marca' in marca:
            producto.marca = marca
        if 'modelo' in modelo:
            producto.modelo = modelo
        if 'especificaciones' in especificaciones:
            producto.especificaciones = especificaciones
        db.session.commit()
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
