import os
from sqlalchemy import create_engine
from models import Game, Base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

def create_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

create_tables()