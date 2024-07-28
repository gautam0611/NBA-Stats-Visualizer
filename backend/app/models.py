"""
This file contains the sql alchemy models
"""
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Conference(Base):
    __tablename__="Conference"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    division = relationship('Division', backref='Conference')

class Division(Base):
    __tablename__="Division"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    conference_id = Column(Integer, ForeignKey('Conference.id'))
    conference = relationship("Conference", backref="Division")

# class Team(Base):
#     __tablename__="Team"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     division_id = Column(Integer, ForeignKey('Conference.id'))
#     division = relationship("Division", back_populates="team")

# class Season(Base):
#     __tablename__="Season"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     team_id = Column(Integer, ForeignKey('Team.id'))
#     team = relationship("Team", back_populates="Season")

# class Roster(Base):
#     __tablename__="Roster"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     season_id = Column(Integer, ForeignKey('Season.id'))
#     season = relationship("Season", back_populates="Roster")

# class Games(Base):
#     __tablename__="Games"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     season_id = Column(Integer, ForeignKey('Season.id'))
#     season = relationship("Season", back_populates="Games")

# class Record(Base):
#     __tablename__="Record"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     season_id = Column(Integer, ForeignKey('Season.id'))
#     season = relationship("Season", back_populates="Record")

# class Player(Base):
#     __tablename__="Player"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     points = Column(DECIMAL(10, 2))
#     rebounds = Column(DECIMAL(10, 2))
#     assists = Column(DECIMAL(10, 2))
#     roster_id = Column(Integer, ForeignKey('Roster.id'))
#     roster = relationship("Roster", back_populates="Player")
    




