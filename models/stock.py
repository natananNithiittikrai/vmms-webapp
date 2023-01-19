from sqlalchemy import Column, INTEGER, ForeignKey
from models.base import Base


class Stock(Base):

    __tablename__ = 'stocks'

    vm_id = Column(INTEGER, ForeignKey('vending_machines.id'), primary_key = True)
    prod_id = Column(INTEGER, ForeignKey('products.id'), primary_key = True)
    stock = Column(INTEGER)

    def __repr__(self):
        return f'<Stock {(self.vm_id, self.prod_id)}>'
