"""
This file contains the sql alchemy models we use so that we don't need to use direct sql
"""

from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Conference(Base):
    __tablename__ = "Conference"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    division = relationship("Division", backref="Conference")


class Division(Base):
    __tablename__ = "Division"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    conference_id = Column(Integer, ForeignKey("Conference.id"))
    conference = relationship("Conference", backref="Division")


class Team(Base):
    __tablename__ = "Team"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    division_id = Column(Integer, ForeignKey("Division.id"))
    division = relationship("Division", backref="Team")


class Season(Base):
    __tablename__ = "Season"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    player = relationship("Player", backref="Season")
    games = relationship("Games", backref="Season")
    record = relationship("Record", backref="Season")


class Player(Base):
    __tablename__ = "Player"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    points = Column(DECIMAL(10, 2))
    rebounds = Column(DECIMAL(10, 2))
    assists = Column(DECIMAL(10, 2))
    season_id = Column(Integer, ForeignKey("Season.id"))
    team_id = Column(Integer, ForeignKey("Team.id"))
    season = relationship("Season", backref="Player")
    team = relationship("Team", backref="Player")


class Games(Base):
    __tablename__ = "Games"
    id = Column(Integer, primary_key=True, index=True)
    opponent = Column(String(255))
    game_date = Column(String(255))
    result = Column(String(255))
    score = Column(String(255))
    season_id = Column(Integer, ForeignKey("Season.id"))
    team_id = Column(Integer, ForeignKey("Team.id"))
    season = relationship("Season", backref="Games")
    team = relationship("Team", backref="Games")


class Record(Base):
    __tablename__ = "Record"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    season_id = Column(Integer, ForeignKey("Season.id"))
    team_id = Column(Integer, ForeignKey("Team.id"))
    season = relationship("Season", backref="Record")
    team = relationship("Team", backref="Record")
