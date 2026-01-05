from typing import List, Optional
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select

from . import models, schemas

def create_exercise(db: Session, exercise: schemas.ExerciseCreate) -> models.Exercise:
    db_exercise = models.Exercise(name=exercise.name)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def get_exercise(db: Session, exercise_id: int) -> Optional[models.Exercise]:
    return db.get(models.Exercise, exercise_id)


def get_exercises(db: Session, skip: int = 0, limit: int = 100) -> List[models.Exercise]:
    return db.exec(select(models.Exercise).offset(skip).limit(limit)).all()

def delete_exercise(db: Session, exercise_id: int) -> None:
    exercise = get_exercise(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db.delete(exercise)
    db.commit()



def create_workout(db: Session, workout: schemas.WorkoutCreate) -> models.Workout:
    workout_date = workout.date or date.today()
    db_workout = models.Workout(date=workout_date)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


#workout

def get_workout(db: Session, workout_id: int) -> Optional[models.Workout]:
    return db.get(models.Workout, workout_id)


def get_workout_by_date(db: Session, workout_date: date) -> Optional[models.Workout]:
    return db.exec(select(models.Workout).where(models.Workout.date == workout_date)).first()


def get_workouts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Workout]:
    return db.exec(select(models.Workout).offset(skip).limit(limit)).all()


# sets


def create_set(db: Session, set_in: schemas.SetCreate) -> models.Set:
    # Determine the date for the workout
    workout_date = set_in.date or date.today()

    # Check if a workout exists for that date
    workout = get_workout_by_date(db, workout_date)
    if not workout:
        # Create a new workout for that date
        workout = models.Workout(date=workout_date)
        db.add(workout)
        db.commit()
        db.refresh(workout)

    # Create the set attached to the workout
    db_set = models.Set(
        workout_id=workout.id,
        exercise_id=set_in.exercise_id,
        reps=set_in.reps,
        weight=set_in.weight,
        unit=set_in.unit,
        date=workout_date
    )

    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set


def get_set(db: Session, set_id: int) -> Optional[models.Set]:
    return db.get(models.Set, set_id)


def get_sets_by_workout(db: Session, workout_id: int) -> List[models.Set]:
    return db.exec(select(models.Set).where(models.Set.workout_id == workout_id)).all()


def get_sets_by_exercise(db: Session, exercise_id: int) -> List[models.Set]:
    return db.exec(select(models.Set).where(models.Set.exercise_id == exercise_id)).all()


def delete_set(db: Session, set_id: int) -> bool:
    db_set = get_set(db, set_id)
    if not db_set:
        raise HTTPException(status_code=404, detail="Set not found")
    db.delete(db_set)
    db.commit()
    return True

