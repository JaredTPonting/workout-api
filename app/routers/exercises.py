from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, database
from ..security import get_current_active_user
from ..models import User

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.post("/", response_model=schemas.ExerciseRead)
def create_exercise(
    exercise: schemas.ExerciseCreate,
    db: Session = Depends(database.get_session),
    current_user: User = Depends(get_current_active_user)
):
    db_exercise = crud.create_exercise(db, exercise)
    return db_exercise


@router.get("/", response_model=List[schemas.ExerciseRead])
def list_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_session)):
    return crud.get_exercises(db, skip=skip, limit=limit)


@router.get("/{exercise_id}", response_model=schemas.ExerciseRead)
def get_exercise(exercise_id: int, db: Session = Depends(database.get_session)):
    db_exercise = crud.get_exercise(db, exercise_id)
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return db_exercise

@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(database.get_session),
    current_user: User = Depends(get_current_active_user)
):
    crud.delete_exercise(db, exercise_id)


@router.put("/{exercise_id}", response_model=schemas.ExerciseRead)
def put_exercise(
    exercise_id: int,
    exercise_update: schemas.ExerciseUpdate,
    db: Session = Depends(database.get_session),
    current_user: User = Depends(get_current_active_user)
):
    return crud.update_exercise(db, exercise_id, exercise_update)
