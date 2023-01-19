from sqlalchemy import Column, INTEGER, VARCHAR
from models.base import Base


class VendingMachine(Base):

    __tablename__ = 'vending_machines'

    id = Column(INTEGER, primary_key = True, autoincrement = True)
    name = Column(VARCHAR(50))
    location = Column(VARCHAR(100))

    def __init__(self, vm_id, name, location):
        self.vm_id = vm_id
        self.name = name
        self.location = location

    def __repr__(self):
        return f'<VendingMachine {self.id}>'
