from sqlalchemy import create_engine
from . import Game, Base
import dataset
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

class Database:
    def __init__(self):
        self._db = dataset.connect(DATABASE_URL)

    def table(self, table):
        """
        TODO: Docstring
        """
        if table in self._db.tables:
            return self._db[table]
        return None

    def create(self):
        """
        TODO: Docstring
        """
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)