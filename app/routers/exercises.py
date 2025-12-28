from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app import crud, models, schemas
from app.database import get_session

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=List[schemas.ExerciseRead])
def read_exercises(session: Session = Depends(get_session)):
    return crud.get_exercises(session)


@router.get("/{exercise_id}", response_model=schemas.ExerciseRead)
def read_exercise(exercise_id: int, session: Session = Depends(get_session)):
    exercise = crud.get_exercise_by_id(session, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.post("/", response_model=schemas.ExerciseRead)
def create_exercise(exercise_in: schemas.ExerciseCreate, session: Session = Depends(get_session)):
    return crud.create_exercise(session, exercise_in)
