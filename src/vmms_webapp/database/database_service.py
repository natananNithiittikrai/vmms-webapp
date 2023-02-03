"""Database Service.

This script allows the user to create and initialize database as well as
interact with database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vmms_webapp.database import utils
from vmms_webapp.models.base import Base


class DatabaseService:
    """A class used to handle database service.

    Attributes:
        uri (str): A path to database
        session (sessionmaker): a session factory to create session for database connection
    """

    def __init__(self, uri: str, default_populate: bool = True) -> None:
        """Initialize DatabaseService.

        Args:
            uri (str): A path to database
            default_populate (bool): A flag to tell if the database should be populate by the predefined data
                (default is True)
        """
        self.uri = uri
        self.session = self.init()
        if default_populate:
            utils.populate_products(self)

    def init(self) -> sessionmaker:
        """Initialize database and returns session factory.

        Returns:
            sessionmaker: a session factory to create session for database connection
        """
        try:
            # setup database
            engine = create_engine(
                self.get_uri(), connect_args={"check_same_thread": False}
            )
            # create tables
            Base.metadata.create_all(engine, checkfirst=True)
            return sessionmaker(bind=engine)
        except Exception as e:
            print("init:", e)

    def get_uri(self) -> str:
        """Get the database uri.

        Returns:
            str: The database uri
        """
        return self.uri

    def get_session(self) -> sessionmaker:
        """Get the database session maker.

        Returns:
            sessionmaker: a session factory to create session for database connection
        """
        return self.session
