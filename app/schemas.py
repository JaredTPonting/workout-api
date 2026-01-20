import datetime
from typing import Optional, List
from pydantic import BaseModel
from .models import WeightUnit

# User

class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str


# Exercise
class ExerciseCreate(BaseModel):
    name: str


class ExerciseRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ExerciseUpdate(BaseModel):
    name: str


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
