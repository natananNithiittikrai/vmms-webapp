from sqlalchemy import Column, INTEGER, ForeignKey
from models.base import Base


class Stock(Base):
    __tablename__ = 'stocks'

    vm_id = Column(INTEGER, ForeignKey('vending_machines.id'), primary_key=True)
    prod_id = Column(INTEGER, ForeignKey('products.id'), primary_key=True)
    stock = Column(INTEGER)

    def __init__(self, vm_id: int, prod_id: int, stock: int) -> None:
        self.vm_id = vm_id
        self.prod_id = prod_id
        self.stock = stock

    def __repr__(self) -> str:
        return f'<Stock {(self.vm_id, self.prod_id)}: {self.stock}>'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Stock):
            return self.vm_id == other.vm_id and self.prod_id == other.prod_id
        return False

    def to_dict(self) -> dict:
        return {
            'vm_id': self.vm_id,
            'prod_id': self.prod_id,
            'stock': self.stock
        }
