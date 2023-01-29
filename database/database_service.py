from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import utils
from models.base import Base


class DatabaseService:

    def __init__(self, uri, default_populate=True):
        self.uri = uri
        self.session = self.init()
        if default_populate:
            utils.populate_products(self)

    def init(self):
        try:
            # setup database
            engine = create_engine(self.get_uri(), connect_args={'check_same_thread': False})
            # create tables
            Base.metadata.create_all(engine, checkfirst=True)
            return sessionmaker(bind=engine)
        except Exception as e:
            print('init:', e)

    def get_uri(self):
        return self.uri

    def get_session(self):
        return self.session
