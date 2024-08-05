from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# GET requests
@app.get("/conference/{conference_name}", response_model=schemas.Conference)
def get_conference(conference_name: str, db: Session = Depends(get_db)):
    db_conference = crud.get_conference(db, conference_name)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_conference


@app.get("/division/{division_name}", response_model=schemas.Division)
def get_division(division_name: str, db: Session = Depends(get_db)):
    db_division = crud.get_division(db, division_name)
    if db_division is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_division


@app.get("/all_teams/{division_name}", response_model=schemas.Team)
def get_all_teams(division_name: int, db: Session = Depends(get_db)):
    db_all_teams = crud.get_all_teams(db, division_name)
    if db_all_teams is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_all_teams


@app.get("/team/{team_name}", response_model=schemas.Team)
def get_team(team_name: str, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_name)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_team


@app.get("/season/{season_name}", response_model=schemas.Season)
def get_season(season_name: str, db: Session = Depends(get_db)):
    db_season = crud.get_season(db, season_name)
    if db_season is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_season


@app.get("/record/{season_name}/{team_name}", response_model=schemas.Record)
def get_record(season_name: str, team_name: str, db: Session = Depends(get_db)):
    db_record = crud.get_record(db, season_name, team_name)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_record


@app.get("/games/{season_name}?{team_name}", response_model=schemas.Games)
def get_games(season_name: str, team_name: str, db: Session = Depends(get_db)):
    db_games = crud.get_games(db, season_name, team_name)
    if db_games is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_games


# -----------------------------------------------------------------------------------------------


# 1) POST/conference
@app.post("/conference/", response_model=schemas.Conference)
def create_conference(
    conference: schemas.ConferenceCreate, db: Session = Depends(get_db)
):
    return crud.create_conference(db=db, conference=conference)


# 2) POST/division
@app.post("/division/{conference_id}", response_model=schemas.Division)
def create_division(division: schemas.DivisionCreate, db: Session = Depends(get_db)):
    # Check if the conference exists
    conference = (
        db.query(models.Conference)
        .filter(models.Conference.id == division.conference_id)
        .first()
    )
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")

    division_create = schemas.DivisionCreate(
        name=division.name, conference_id=division.conference_id
    )
    return crud.create_division(db=db, division=division_create)


# 3) POST/team
@app.post("/team/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    # Check if the division exists
    division = (
        db.query(models.Division).filter(models.Division.id == team.division_id).first()
    )
    if not division:
        raise HTTPException(status_code=404, detail="Division not found")

    team_create = schemas.TeamCreate(name=team.name, division_id=team.division_id)

    return crud.create_team(db=db, team=team_create)


# 4) POST/record/{season_id}
@app.post("/record/{season_id}?{team_id}", response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    # Check if the season exists for the specified team
    season = (
        db.query(models.Season)
        .filter(
            and_(models.Season.id == record.season_id, models.Team.id == record.team_id)
        )
        .first()
    )
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    record_create = schemas.RecordCreate(
        name=record.name, season_id=record.season_id, team_id=record.team_id
    )

    return crud.create_record(db=db, record=record_create)


# # 5) POST/season
# @app.post("/season/", response_class=schemas.Season)
# def create_season(season: schemas.SeasonCreate, db: Session = Depends(get_db)):
#     return crud.create_season(db, season=season)


# @FIXME need to address season because of team_id down below
# 6) POST/games/{season_id}?{team_id}
@app.post("/games/{season_id}?{team_id}", response_model=schemas.Games)
def create_games(games: schemas.GamesCreate, db: Session = Depends(get_db)):
    # Check if the season exists for the specified team
    season = (
        db.query(models.Season)
        .join(models.Team, models.Season.team_id == models.Team.id)
        .filter(
            and_(models.Season.id == games.season_id, models.Team.id == games.team_id)
        )
        .first()
    )
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    games_create = schemas.GamesCreate(
        name=games.name, season_id=games.season_id, team_id=games.team_id
    )

    return crud.create_game(db, game=games_create)


# 7 POST/player/{season_id}?{team_id}
@app.post("/player/{season_id}?{team_id}", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    # Check if the season exists for the specified team
    season = (
        db.query(models.Season)
        .join(models.Team, models.Season.team_id == models.Team.id)
        .filter(
            and_(models.Season.id == player.season_id, models.Team.id == player.team_id)
        )
        .first()
    )
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    player_create = schemas.PlayerCreate(
        name=player.name, season_id=player.season_id, team_id=player.team_id
    )

    return crud.create_player(db, player=player_create)
