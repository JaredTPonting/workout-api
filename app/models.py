import datetime
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import Mapped


class WeightUnit(str, Enum):
    KG = "kg"
    LBS = "lbs"


class Exercise(SQLModel, table=True):
    __tablename__ = "exercises"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    # Relationship
    sets: Mapped[List["Set"]] = Relationship(back_populates="exercise")


class Workout(SQLModel, table=True):
    __tablename__ = "workouts"

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime.date = Field(index=True)

    # Relationship
    sets: Mapped[List["Set"]] = Relationship(back_populates="workout")


class Set(SQLModel, table=True):
    __tablename__ = "sets"

    id: Optional[int] = Field(default=None, primary_key=True)
    workout_id: int = Field(foreign_key="workouts.id", index=True)
    exercise_id: int = Field(foreign_key="exercises.id", index=True)
    reps: int
    weight: float
    unit: WeightUnit
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, index=True)

    # Relationships
    workout: Mapped["Workout"] = Relationship(back_populates="sets")
    exercise: Mapped["Exercise"] = Relationship(back_populates="sets")

