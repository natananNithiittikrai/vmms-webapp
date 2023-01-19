from sqlalchemy import Column, INTEGER, VARCHAR, DECIMAL
from models.base import Base


class Product(Base):

    __tablename__ = 'products'

    id = Column(INTEGER, primary_key = True, autoincrement = True)
    name = Column(VARCHAR(50))
    price = Column(DECIMAL(10, 5))

    def __init__(self, prod_id, name, price):
        self.prod_id = prod_id
        self.name = name
        self.price = price

    def __repr__(self):
        return f'<Product {self.name}>'
