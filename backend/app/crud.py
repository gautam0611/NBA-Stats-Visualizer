"""
This file contains the CRUD operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.schemas import (
    ConferenceCreate,
    DivisionCreate,
    GamesCreate,
    PlayerCreate,
    RecordCreate,
    SeasonCreate,
    TeamCreate,
)

from . import models


# GET /{conference_id}
# get the specified conference
def get_conference(db: Session, conference_id: int):
    return (
        db.query(models.Conference)
        .filter(models.Conference.id == conference_id)
        .first()
    )


# GET /{division_id}
# get the specified division
def get_division(db: Session, division_id: int):
    return db.query(models.Division).filter(models.Division.id == division_id).first()


# GET /teams/{conference_id}
# get all of the teams in the specified division
def get_all_teams(db: Session, division_id: int):
    return db.query(models.Team).filter(models.Team.division_id == division_id).all()


# GET /{team_id}?{conference_id}
# get a specific team from a specific division
def get_team(db: Session, team_id: int, division_id: int):
    return (
        db.query(models.Team)
        .filter(and_(models.Team.id == team_id, models.Team.division_id == division_id))
        .first()
    )


# GET /record/{season_id}?{team_id}
# gets the record for the specified season
def get_record(db: Session, season_id: int, team_id: int):
    return (
        db.query(models.Record)
        .join(models.Season, models.Record.season_id == models.Season.id)
        .join(models.Team, models.Record.team_id == models.Team.id)
        .filter(
            and_(
                models.Record.season_id == season_id,
                models.Record.team_id == team_id,
            )
        )
        .first()
    )


# GET /games/{season_id}?{team_id}
# get the games for the specified season
def get_games(db: Session, season_id: int, team_id: int):
    return (
        db.query(models.Games)
        .join(models.Season, models.Games.season_id == models.Season.id)
        .join(models.Team, models.Games.team_id == models.Team.id)
        .filter(
            and_(
                models.Games.season_id == season_id,
                models.Games.team_id == team_id,
            )
        )
        .all()
    )


# GET /players/{team_id}?{season_id}
# get a list of players on a team for a specific season
def get_players(db: Session, team_id: int, season_id: int):
    return (
        db.query(models.Player)
        .join(models.Season, models.Player.season_id == models.Season.id)
        .join(models.Team, models.Season.team_id == models.Team.id)
        .filter(and_(models.Team.id == team_id, models.Season.id == season_id))
        .all()
    )


# # --------------------------------------------------------------------------------------


# POST /conference
def create_conference(db: Session, conference: ConferenceCreate):
    db_conference = models.Conference(name=conference.name)
    db.add(db_conference)
    db.commit()
    db.refresh(db_conference)
    return db_conference


# POST /division
def create_division(db: Session, division: DivisionCreate):
    db_division = models.Division(
        name=division.name, conference_id=division.conference_id
    )
    db.add(db_division)
    db.commit()
    db.refresh(db_division)
    return db_division


# POST /team
def create_team(db: Session, team: TeamCreate):
    db_team = models.Team(name=team.name, division_id=team.division_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


# @FIXME
# # POST /season/{team_id}
# def create_season(db: Session, season: SeasonCreate):
#     db_season = models.Season(name=season.name)
#     db.add(db_season)
#     db.commit()
#     db.refresh(db_season)
#     return db_season


# POST /record
def create_record(db: Session, record: RecordCreate):
    db_record = models.Record(
        name=record.name, season_id=record.season_id, team_id=record.team_id
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


# POST /player/{team_id}?{season_id}
def create_player(db: Session, player: PlayerCreate):
    db_player = models.Player(
        name=player.name,
        points=player.points,
        rebounds=player.rebounds,
        assists=player.assists,
        season_id=player.season_id,
        team_id=player.team_id,
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


# POST /game/{season_id}?{team_id}
def create_game(db: Session, game: GamesCreate):
    db_game = models.Games(
        result=game.result,
        opponent=game.opponent,
        score=game.score,
        season_id=game.season_id,
        team_id=game.team_id,
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game
