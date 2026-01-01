import datetime
from typing import Optional, List
from pydantic import BaseModel
from .models import WeightUnit


# Exercise
class ExerciseCreate(BaseModel):
    name: str


class ExerciseRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# Workout
class WorkoutCreate(BaseModel):
    date: Optional[datetime.date] = None


class WorkoutRead(BaseModel):
    id: int
    date: datetime.date

    class Config:
        orm_mode = True


# Set
class SetCreate(BaseModel):
    exercise_id: int
    reps: int
    weight: float
    unit: WeightUnit
    date: Optional[datetime.date] = None


class SetRead(BaseModel):
    id: int
    workout_id: int
    exercise_id: int
    reps: int
    weight: float
    unit: WeightUnit
    created_at: datetime.datetime

    class Config:
        orm_mode = True
