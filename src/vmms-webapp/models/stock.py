"""Stock."""

from models.base import Base
from sqlalchemy import INTEGER, Column, ForeignKey


class Stock(Base):
    """
    A class used to represent a product.

    Attributes:
        vm_id (int): A vending machine identification
        prod_id (str): A product identification
        stock (float): A product stock inside the vending machine
    """

    __tablename__ = "stocks"

    vm_id = Column(INTEGER, ForeignKey("vending_machines.id"), primary_key=True)
    prod_id = Column(INTEGER, ForeignKey("products.id"), primary_key=True)
    stock = Column(INTEGER)

    def __init__(self, vm_id: int, prod_id: int, stock: int) -> None:
        """Initialize Stock.

        Args:
            vm_id (int): A vending machine identification
            prod_id (str): A product identification
            stock (float): A product stock inside the vending machine
        """
        self.vm_id = vm_id
        self.prod_id = prod_id
        self.stock = stock

    def __repr__(self) -> str:
        """Return a string as a representation of the object.

        Returns:
            str: A string representation of the object
        """
        return f"<Stock {(self.vm_id, self.prod_id)}: {self.stock}>"

    def __eq__(self, other: object) -> bool:
        """Check equality of both instances.

        Returns:
            bool: True if the both instances are equal else False
        """
        if isinstance(other, Stock):
            return self.vm_id == other.vm_id and self.prod_id == other.prod_id
        return False

    def to_dict(self) -> dict:
        """Convert the object to dictionary.

        Returns:
            dict: A dictionary representing the object
        """
        return {"vm_id": self.vm_id, "prod_id": self.prod_id, "stock": self.stock}
