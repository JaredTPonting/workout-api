from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import crud, schemas, database
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.post("/", response_model=schemas.WorkoutRead)
def create_workout(workout: schemas.WorkoutCreate, user: User = Depends(get_current_user), db: Session = Depends(database.get_session)):
    db_workout = crud.create_workout(db, workout)
    return db_workout


@router.get("/", response_model=List[schemas.WorkoutRead])
def list_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_session)):
    return crud.get_workouts(db, skip=skip, limit=limit)


@router.get("/{workout_id}", response_model=schemas.WorkoutRead)
def get_workout(workout_id: int, db: Session = Depends(database.get_session)):
    db_workout = crud.get_workout(db, workout_id)
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return db_workout


@router.get("/by-date/{workout_date}", response_model=schemas.WorkoutRead)
def get_workout_by_date(workout_date: date, db: Session = Depends(database.get_session)):
    db_workout = crud.get_workout_by_date(db, workout_date)
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found for this date")
    return db_workout
