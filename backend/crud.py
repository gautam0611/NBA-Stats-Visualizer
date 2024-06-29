"""
This file contains the CRUD operations.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas

# GET /{conference_id}
# get the specified conference
def get_conference(db: Session, conference_id: int):
    return db.query(models.Conference).filter(models.Conference.id == conference_id).first()

# GET /teams/{conference_id}
# get all of the teams in the specified conference 
def get_teams(db: Session, conference_id: int):
    return db.query(models.Team).filter(models.Team.conference_id == conference_id).all()

# GET /{team_id}?{conference_id}
# get a specific team from a specific conference 
def get_team_from_conference(db: Session, team_id: int, conference_id: int):
    return db.query(models.Team).filter(and_(models.Team.id == team_id, models.Team.conference_id == conference_id)).first()

# GET /record/{season_id}?{team_id}
# gets the record for the specified season
# @FIXME not the correct query
def get_record(db: Session, season_id: int):
    return db.query(models.Team).join(models.Season, models.Team.id == models.Season.team_id).join(models.Record, models.Season.id == models.Record.season_id)

# GET /roster/{season_id}?{team_id}
# get the roster for that specified season
def get_roster(db: Session, season_id: int, team_id: int):
    return db.query(models.Roster).join(models.Season, models.Roster.season_id == models.Season.id).filter(and_(models.Season.id == season_id, models.Season.team_id == team_id)).first()

# GET /games/{season_id}?{team_id}
# get the games for the specified season
def get_games(db: Session, season_id: int, team_id: int):
    return db.query(models.Games).join(models.Season, models.Games.season_id == models.Season.id).filter(and_(models.Season.id == season_id, models.Season.team_id == team_id)).first()



