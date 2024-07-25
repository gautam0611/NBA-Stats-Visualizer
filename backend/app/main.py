from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from . database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# GET requests 
@app.get("/conference/{conference_id}", response_model=schemas.Conference)
def get_conference(conference_id: int, db: Session = Depends(get_db)):
    db_conference = crud.get_conference(db, conference_id)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_conference

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
def get_record(record_id: int, season_id: int, team_id: int, db: Session = Depends(get_db)):
    db_record = crud.get_record(db, record_id, season_id, team_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_record

@app.get("/roster/{roster_id}/{season_id}/{team_id}", response_model=schemas.Roster)
def get_roster(roster_id: int, season_id: int, team_id: int, db: Session = Depends(get_db)):
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

# POST requests (*TO-DO*)

# 1) POST/conference

# 2) POST/teams

# 3) POST/{season_id}/record

# 2) POST/{season_id}/roster

# 3) POST/{season_id}/games