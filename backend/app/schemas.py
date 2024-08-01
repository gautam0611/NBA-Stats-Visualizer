"""
This file contains the pydantic schemas.
"""

from decimal import Decimal
from pydantic import BaseModel


class ConferenceBase(BaseModel):
    name: str


class Conference(ConferenceBase):
    id: int

    class Config:
        from_attributes = True


class ConferenceCreate(ConferenceBase):
    pass


class DivisionBase(BaseModel):
    name: str


class Division(DivisionBase):
    id: int
    conference_id: int

    class Config:
        from_attributes = True


class DivisionCreate(DivisionBase):
    conference_id: int


class TeamBase(BaseModel):
    name: str


class Team(TeamBase):
    id: int
    division_id: (
        int  # @FIXME figure out what needs to be done when you have foreign keys
    )

    class Config:
        from_attributes = True


class TeamCreate(TeamBase):
    division_id: int


class SeasonBase(BaseModel):
    name: str


class Season(SeasonBase):
    id: int
    team_id: int

    class Config:
        from_attributes = True


class SeasonCreate(SeasonBase):
    team_id: int


# class RosterBase(BaseModel):
#     name: str


# class Roster(RosterBase):
#     id: int
#     season_id: int

#     class Config:
#         from_attributes = True


# class RosterCreate(RosterBase):
#     season_id: int


class RecordBase(BaseModel):
    name: str


class Record(RecordBase):
    id: int
    season_id: int

    class Config:
        from_attributes = True


class RecordCreate(RecordBase):
    season_id: int
    team_id: int


class GamesBase(BaseModel):
    name: str


class Games(GamesBase):
    id: int
    season_id: int


class GamesCreate(GamesBase):
    season_id: int
    team_id: int


class PlayerBase(BaseModel):
    name: str
    points: Decimal
    rebounds: Decimal
    assists: Decimal


class Player(PlayerBase):
    id: int
    season_id: int


class PlayerCreate(PlayerBase):
    season_id: int
    team_id: int
