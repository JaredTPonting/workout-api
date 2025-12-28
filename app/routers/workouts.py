from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app import crud, schemas
from app.database import get_session

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.get("/", response_model=List[schemas.WorkoutRead])
def read_workouts(session: Session = Depends(get_session)):
    return crud.get_workouts(session)

@router.get("/{workout_id}", response_model=schemas.WorkoutRead)
def read_workout(workout_id: int, session: Session = Depends(get_session)):
    workout = crud.get_workout_by_id(session, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.post("/", response_model=schemas.WorkoutRead)
def create_workout(workout_in: schemas.WorkoutCreate, session: Session = Depends(get_session)):
    return crud.create_workout(session, workout_in)