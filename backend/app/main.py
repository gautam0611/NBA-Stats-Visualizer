from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# GET requests
@app.get("/conference/{conference_id}", response_model=schemas.Conference)
def get_conference(conference_id: int, db: Session = Depends(get_db)):
    db_conference = crud.get_conference(db, conference_id)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_conference


@app.get("/division/{division_id}", response_model=schemas.Division)
def get_division(division_id: int, db: Session = Depends(get_db)):
    db_division = crud.get_division(db, division_id)
    if db_division is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_division


@app.get("/all_teams/{conference_id}", response_model=schemas.Team)
def get_all_teams(conference_id: int, db: Session = Depends(get_db)):
    db_all_teams = crud.get_all_teams(db, conference_id)
    if db_all_teams is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_all_teams


@app.get("/team/{team_id}/{conference_id}", response_model=schemas.Team)
def get_team(team_id: int, conference_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id, conference_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_team


@app.get("/record/{record_id}/{season_id}/{team_id}", response_model=schemas.Record)
def get_record(
    record_id: int, season_id: int, team_id: int, db: Session = Depends(get_db)
):
    db_record = crud.get_record(db, record_id, season_id, team_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_record


@app.get("/roster/{roster_id}/{season_id}/{team_id}", response_model=schemas.Roster)
def get_roster(
    roster_id: int, season_id: int, team_id: int, db: Session = Depends(get_db)
):
    db_roster = crud.get_roster(db, roster_id, season_id, team_id)
    if db_roster is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_roster


@app.get("/games/{season_id}?{team_id}", response_model=schemas.Games)
def get_games(season_id: int, team_id: int, db: Session = Depends(get_db)):
    db_games = crud.get_games(db, season_id, team_id)
    if db_games is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_games


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


# 3) POST/teams
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
@app.post("/record/{season_id}", response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    # Check if the division exists
    season = (
        db.query(models.Season).filter(models.Season.id == record.season_id).first()
    )
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    record_create = schemas.RecordCreate(name=record.name, season_id=record.season_id)

    return crud.create_record(db=db, record=record_create)


# 5) POST/games/{season_id}?{team_id}
@app.post("/games/{season_id}?{team_id}", response_model=schemas.Games)
def create_games(games: schemas.GamesCreate, db: Session = Depends(get_db)):
    return crud.create_game(db, game=games)


"""
@FIXME address the create functions
"""

# 4 POST/season/{team_id}

# 6 POST/player/{season_id}?{team_id}


# # 4) POST/roster/{season_id}
# @app.post("/roster/{season_id}", response_model=schemas.Roster)
# def create_roster(roster: schemas.Roster, db: Session = Depends(get_db)):
#     return crud.create_roster(db, roster=roster)
