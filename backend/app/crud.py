"""
This file contains the CRUD operations.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.schemas import ConferenceCreate, DivisionCreate

# from app.schemas import ConferenceCreate, GamesCreate, PlayerCreate, RecordCreate, RosterCreate, SeasonCreate, TeamCreate
from . import models
# from app.models import Conference, Record, Team, Roster, Games, Player, Season

# GET /{conference_id}
# get the specified conference
def get_conference(db: Session, conference_id: int):
    return db.query(models.Conference).filter(models.Conference.id == conference_id).first()

# GET /{division_id}
# get the specified division
def get_division(db: Session, division_id: int):
    return db.query(models.Division).filter(models.Division.id == division_id).first()

# # GET /teams/{conference_id}
# # get all of the teams in the specified conference 
# def get_all_teams(db: Session, conference_id: int):
#     return db.query(models.Team).filter(models.Team.conference_id == conference_id).all()

# # GET /{team_id}?{conference_id}
# # get a specific team from a specific conference 
# def get_team(db: Session, team_id: int, conference_id: int):
#     return db.query(models.Team).filter(and_(models.Team.id == team_id, models.Team.conference_id == conference_id)).first()

# # GET /record/{record_int}?{season_id}?{team_id}
# # gets the record for the specified season
# def get_record(db: Session, record_id: int, season_id: int, team_id: int):
#     return db.query(models.Record).join(models.Season, models.Record.season_id == models.Season.id).filter(and_(models.Record.id == record_id, models.Season.id == season_id, models.Season.team_id == team_id)).first()

# # GET /roster/{roster_id}?{season_id}?{team_id}
# # get the roster for that specified season
# def get_roster(db: Session, roster_id: int, season_id: int, team_id: int):
#     return db.query(models.Roster).join(models.Season, models.Roster.season_id == models.Season.id).filter(and_(models.Roster.id == roster_id, models.Season.id == season_id, models.Season.team_id == team_id)).first()

# # GET /games/{season_id}?{team_id}
# # get the games for the specified season
# def get_games(db: Session, season_id: int, team_id: int):
#     return db.query(models.Games).join(models.Season, models.Games.season_id == models.Season.id).filter(and_(models.Season.id == season_id, models.Season.team_id == team_id)).all()

# # GET /players/{team_id}?{season_id}
# # get a list of players on a team for a specific season
# def get_players(db: Session, team_id: int, season_id: int):
#     return db.query(models.Player).join(models.Roster, models.Player.roster_id == models.Roster.id).join(models.Season, models.Roster.season_id == models.Season.id).join(models.Team, models.Season.team_id == models.Team.id).filter(and_(models.Team.id == team_id, models.Season.id == season_id)).all()

# POST /conference
def create_conference(db: Session, conference: ConferenceCreate):
    db_conference = models.Conference(name=conference.name)
    db.add(db_conference)
    db.commit()
    db.refresh(db_conference)
    return db_conference

# POST /division
def create_division(db: Session, division: DivisionCreate):
    db_division = models.Division(name=division.name, conference_id=division.conference_id)
    db.add(db_division)
    db.commit()
    db.refresh(db_division)
    return db_division

# # POST /team
# def create_team(db: Session, team: TeamCreate):
#     db_team = models.Team(name=team.name)
#     db.add(db_team)
#     db.commit()
#     db.refresh(db_team)
#     return db_team

# # POST /season/{season_id}?{team_id}
# def create_season(db: Session, season: SeasonCreate):
#     db_season = Season(name=season.name)
#     db.add(db_season)
#     db.commit()
#     db.refresh(db_season)
#     return db_season

# """
# @FIXME need to update this so that we can add foreign keys
# """
# # POST /game/{season_id}?{team_id}
# def create_game(db: Session, game: GamesCreate):
#     db_game = Games(name=game.name)
#     db.add(db_game)
#     db.commit()
#     db.refresh(db_game)
#     return db_game

# # POST /player/{team_id}?{season_id}
# def create_player(db: Session, player: PlayerCreate):
#     db_player = Player(name=player.name, points=player.points, rebounds=player.rebounds, assists=player.assists)
#     db.add(db_player)
#     db.commit()
#     db.refresh(db_player)
#     return db_player

# # POST /roster/{roster_id}?{season_id}?{team_id}
# def create_roster(db: Session, roster: RosterCreate):
#     db_roster = Roster(name=roster.name)
#     db.add(db_roster)
#     db.commit()
#     db.refresh(db_roster)
#     return db_roster

# # POST /record
# def create_record(db: Session, record: RecordCreate):
#     db_record = Record(name=record.name)
#     db.add(db_record)
#     db.commit()
#     db.refresh(db_record)
#     return db_record






