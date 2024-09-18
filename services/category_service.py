from repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()

    def create_category(self, name, description):
        return self.repository.create_category(name, description)

    def get_categories(self):
        return self.repository.get_categories()

    def search_categories(self, name_query):
        return self.repository.search_categories(name_query)

    def delete_category(self, id):
        return self.repository.delete_category(id)

    def update_category(self, id, name, description):
        return self.repository.update_category(id, name, description)