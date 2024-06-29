"""
This file contains the CRUD operations.
"""
from sqlalchemy.orm import Session
from . import models, schemas

def get_conference(db: Session, conference_id: int):
    return db.query(models.Conference).filter(models.Conference.id == conference_id).first() 