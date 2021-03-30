from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Battles(Base):
    __tablename__ = "battles"
    battle_id = Column(Integer, primary_key=True)
    date = Column(String)
    battle_timer = Column(Integer, default = 0)
    player_count = Column(Integer)
    is_deleted = Column(Boolean, default=False) 
    participants = relationship("Participants", cascade="all, delete, delete-orphan")

class Participants(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    guild = Column(String)
    player_count = Column(Integer)
    battle_id = Column(Integer, ForeignKey("battles.battle_id"))
    battle = relationship(Battles)

engine = create_engine('sqlite:///fricks.db')

Base.metadata.create_all(engine)
