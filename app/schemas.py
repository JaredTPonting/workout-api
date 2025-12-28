from __future__ import annotations
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from app.models import WeightUnit


# Exercise Schemas
class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Set Schemas
class SetBase(BaseModel):
    reps: int
    weight: float
    unit: WeightUnit
    set_number: int


class SetCreate(SetBase):
    exercise_id: int


class SetRead(SetBase):
    id: int
    exercise: ExerciseRead
    model_config = ConfigDict(from_attributes=True)


# Workout Schemas
class WorkoutBase(BaseModel):
    date: Optional[date] = None


class WorkoutCreate(WorkoutBase):
    sets: List[SetCreate]


class WorkoutRead(WorkoutBase):
    id: int
    sets: List[SetRead]
    model_config = ConfigDict(from_attributes=True)
