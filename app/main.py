import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import exercises, workouts
from app.database import engine
from app import models

models.SQLModel.metadata.create_all(engine)

app = FastAPI(title="Workout Tracker API", version="1.0")

# CORS Configuration
# Allow all origins for now since frontend isn't ready
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(exercises.router)
app.include_router(workouts.router)
