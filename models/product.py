"""Product."""

from sqlalchemy import DECIMAL, INTEGER, VARCHAR, Column

from models.base import Base


class Product(Base):
    """
    A class used to represent a product.

    Attributes:
        id (int): A product identification
        name (str): A product name
        price (float): A product price
    """

    __tablename__ = "products"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50))
    price = Column(DECIMAL(10, 2))

    def __init__(self, id: int, name: str, price: float) -> None:
        """Initialize Product.

        Args:
            id (int): A product identification
            name (str): A product name
            price (float): A product price
        """
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        """Return a string as a representation of the object.

        Returns:
            str: A string representation of the object
        """
        return f"<Product {self.id}: {self.name}>"

    def __eq__(self, other: object) -> bool:
        """Check equality of both instances.

        Returns:
            bool: True if the both instances are equal else False
        """
        if isinstance(other, Product):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        """Return the hash value of the object.

        Returns:
            int: The hash value of the object
        """
        return hash(self.id)

    def to_dict(self) -> dict:
        """Convert the object to dictionary.

        Returns:
            dict: A dictionary representing the object
        """
        return {"name": self.name, "price": self.price}
