"""
This file contains the pydantic schemas.
"""
from decimal import Decimal
from pydantic import BaseModel

class ConferenceBase(BaseModel):
    name: str 

class TeamBase(BaseModel): 
    name: str 
    
class SeasonBase(BaseModel): 
    name: str

class RosterBase(BaseModel): 
    name: str

class GamesBase(BaseModel): 
    name: str

class RecordBase(BaseModel): 
    name: str

class PlayersBase(BaseModel): 
    name: str
    points: Decimal
    rebounds: Decimal
    assists: Decimal





 
