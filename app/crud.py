from typing import List, Optional
from sqlmodel import Session, select, desc
from app import models, schemas


# Exercises
def create_exercise(session: Session, exercise_in: schemas.ExerciseCreate) -> models.Exercise:
    exercise = models.Exercise(name=exercise_in.name)
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise


def get_exercise_by_id(session: Session, exercise_id: int) -> Optional[models.Exercise]:
    return session.get(models.Exercise, exercise_id)


def get_exercises(session: Session) -> List[models.Exercise]:
    statement = select(models.Exercise).order_by(models.Exercise.name)
    return list(session.exec(statement).all())


# Workouts
def create_workout(session: Session, workout_in: schemas.WorkoutCreate) -> models.Workout:
    workout = models.Workout(date=workout_in.date)
    session.add(workout)
    session.commit()
    session.refresh(workout)

    for set_in in workout_in.sets:
        set_obj = models.Set(
            workout_id=workout.id,
            exercise_id=set_in.exercise_id,
            reps=set_in.reps,
            weight=set_in.weight,
            unit=set_in.unit,
            set_number=set_in.set_number,
        )
        session.add(set_obj)

    session.commit()
    session.refresh(workout)
    return workout


def get_workout_by_id(session: Session, workout_id: int) -> Optional[models.Workout]:
    return session.get(models.Workout, workout_id)


def get_workouts(session: Session) -> List[models.Workout]:
    statement = select(models.Workout).order_by(desc(models.Workout.date))
    return list(session.exec(statement).all())
