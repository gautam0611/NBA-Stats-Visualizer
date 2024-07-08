"""
This file contains the pydantic schemas.
"""
from decimal import Decimal
from pydantic import BaseModel

"""
@FIXME: Is there a better way to organize all of this code?
"""

class ConferenceBase(BaseModel):
    name: str 

class Conference(ConferenceBase):
    id: int
    class Config:
        orm_mode=True

class TeamBase(BaseModel): 
    name: str 

class Team(TeamBase):
    id: int
    conference_id: Conference.id # @FIXME figure out what needs to be done when you have foreign keys 
    class Config:
        orm_mode=True
    
class SeasonBase(BaseModel): 
    name: str

class Season(SeasonBase):
    id: int
    team_id: Team.id
    class Config:
        orm_mode=True

class RosterBase(BaseModel): 
    name: str

class Roster(RosterBase):
    id: int
    season_id: Season.id
    class Config:
        orm_mode=True

class RecordBase(BaseModel): 
    name: str

class Record(RecordBase):
    id: int
    season_id: Season.id
    class Config:
        orm_mode=True

class GamesBase(BaseModel): 
    name: str

class Games(GamesBase):
    id: int
    season_id: Season.id

class PlayersBase(BaseModel): 
    name: str
    points: Decimal
    rebounds: Decimal
    assists: Decimal
    roster_id: Roster.id





 
