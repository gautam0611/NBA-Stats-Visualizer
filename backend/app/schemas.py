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
        from_attributes = True

class TeamBase(BaseModel): 
    name: str 

class Team(TeamBase):
    id: int
    conference_id: int # @FIXME figure out what needs to be done when you have foreign keys 
    class Config:
        from_attributes = True
    
class SeasonBase(BaseModel): 
    name: str

class Season(SeasonBase):
    id: int
    team_id: int
    class Config:
        from_attributes = True

class RosterBase(BaseModel): 
    name: str

class Roster(RosterBase):
    id: int
    season_id: int
    class Config:
        from_attributes = True

class RecordBase(BaseModel): 
    name: str

class Record(RecordBase):
    id: int
    season_id: int
    class Config:
        from_attributes = True

class GamesBase(BaseModel): 
    name: str

class Games(GamesBase):
    id: int
    season_id: int

class PlayersBase(BaseModel): 
    name: str
    points: Decimal
    rebounds: Decimal
    assists: Decimal
    roster_id: int





 
