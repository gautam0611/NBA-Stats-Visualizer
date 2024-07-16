"""
This file contains the CRUD operations.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models

# @FIXME fix the to do expressions to include the main table's primary key 

# GET /{conference_id}
# get the specified conference
def get_conference(db: Session, conference_id: int):
    return db.query(models.Conference).filter(models.Conference.id == conference_id).first()

# GET /teams/{conference_id}
# get all of the teams in the specified conference 
def get_all_teams(db: Session, conference_id: int):
    return db.query(models.Team).filter(models.Team.conference_id == conference_id).all()

# GET /{team_id}?{conference_id}
# get a specific team from a specific conference 
def get_team(db: Session, team_id: int, conference_id: int):
    return db.query(models.Team).filter(and_(models.Team.id == team_id, models.Team.conference_id == conference_id)).first()

# GET /record/{record_int}?{season_id}?{team_id}
# gets the record for the specified season
def get_record(db: Session, record_id: int, season_id: int, team_id: int):
    return db.query(models.Record).join(models.Season, models.Record.season_id == models.Season.id).filter(and_(models.Record.id == record_id, models.Season.id == season_id, models.Season.team_id == team_id)).first()

# GET /roster/{roster_id}?{season_id}?{team_id}
# get the roster for that specified season
def get_roster(db: Session, roster_id: int, season_id: int, team_id: int):
    return db.query(models.Roster).join(models.Season, models.Roster.season_id == models.Season.id).filter(and_(models.Roster.id == roster_id, models.Season.id == season_id, models.Season.team_id == team_id)).first()

# GET /games/{season_id}?{team_id}
# get the games for the specified season
def get_games(db: Session, season_id: int, team_id: int):
    return db.query(models.Games).join(models.Season, models.Games.season_id == models.Season.id).filter(and_(models.Season.id == season_id, models.Season.team_id == team_id)).all()



