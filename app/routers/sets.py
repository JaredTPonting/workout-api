from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, database
from ..security import get_current_active_user
from ..models import User

router = APIRouter(prefix="/sets", tags=["Sets"])


@router.post("/", response_model=schemas.SetRead)
def create_set_endpoint(
    set_in: schemas.SetCreate,
    db: Session = Depends(database.get_session),
    current_user: User = Depends(get_current_active_user)
):
    return crud.create_set(db, set_in)


@router.get("/by-workout/{workout_id}", response_model=List[schemas.SetRead])
def get_sets_by_workout(workout_id: int, db: Session = Depends(database.get_session)):
    return crud.get_sets_by_workout(db, workout_id)


@router.get("/by-exercise/{exercise_id}", response_model=List[schemas.SetRead])
def get_sets_by_exercise(exercise_id: int, db: Session = Depends(database.get_session)):
    return crud.get_sets_by_exercise(db, exercise_id)


@router.delete("/{set_id}")
def delete_set(
    set_id: int,
    db: Session = Depends(database.get_session),
    current_user: User = Depends(get_current_active_user)
):
    success = crud.delete_set(db, set_id)
    if not success:
        raise HTTPException(status_code=404, detail="Set not found")
    return {"detail": "Set deleted"}
