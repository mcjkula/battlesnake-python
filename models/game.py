from .base import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

class Game(Base):
    __tablename__ = 'games'

    game_id = Column(String, primary_key=True)
    replay_link = Column(String)
    source = Column(String)
    game_map = Column(String)
    timeout = Column(Integer)
    outcome = Column(Boolean)
    last_turn = Column(Integer)