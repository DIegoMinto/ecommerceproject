from repositories.product_repository import ProductoRepository

class ProductService:
    def __init__(self):
        self.repository = ProductoRepository()

    def create_product(self, nombre, descripcion, precio, stock, imagen_url, categoria_id, marca, modelo, especificaciones):
        return self.repository.crear_producto(nombre, descripcion, precio, stock, imagen_url, categoria_id, marca, modelo, especificaciones)


    def get_products(self):
        return self.repository.obtener_productos()

    def get_product(self, id):
        return self.repository.obtener_producto_por_id(id)

    def delete_product(self, id):
        return self.repository.eliminar_producto(id)

    def update_product(self, id, nombre, descripcion, precio, stock, imagen_url, categoria_id, marca, modelo, especificaciones):
        return self.repository.actualizar_producto(id, nombre, descripcion, precio, stock, imagen_url, categoria_id, marca, modelo, especificaciones)