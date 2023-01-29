from sqlalchemy import Column, INTEGER, VARCHAR, DECIMAL
from models.base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50))
    price = Column(DECIMAL(10, 2))

    def __init__(self, id: int, name: int, price: int) -> None:
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return f'<Product {self.id}: {self.name}>'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Product):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'price': self.price
        }
