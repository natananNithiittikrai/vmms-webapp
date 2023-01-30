"""Vending Machine."""

from sqlalchemy import INTEGER, VARCHAR, Column

from models.base import Base


class VendingMachine(Base):
    """
    A class used to represent a vending machine.

    Attributes:
        name (str): A vending machine name
        location (str): A vending machine location
    """

    __tablename__ = "vending_machines"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50))
    location = Column(VARCHAR(100))

    def __init__(self, name: str, location: str) -> None:
        """Initialize VendingMachine.

        Args:
            name (str): A vending machine name
            location (str): A vending machine location
        """
        self.name = name
        self.location = location

    def __repr__(self) -> str:
        """Return a string as a representation of the object.

        Returns:
            str: A string representation of the object
        """
        return f"<VendingMachine {self.id}: {self.name}>"

    def __eq__(self, other: object) -> bool:
        """Check equality of both instances.

        Returns:
            bool: True if the both instances are equal else False
        """
        if isinstance(other, VendingMachine):
            return self.id == other.id
        return False

    def to_dict(self) -> dict:
        """Convert the object to dictionary.

        Returns:
            dict: A dictionary representing the object
        """
        return {"name": self.name, "location": self.location}
