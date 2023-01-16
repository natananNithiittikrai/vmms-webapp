from product import Product
class VendingMachine:

    def __init__(self, id: int, name: str, location: str, products: dict[Product, int]):
        self.id = id
        self.name = name
        self.location = location
        self.products = products
