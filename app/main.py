import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from app.routers import exercises, workouts, sets
from app.database import engine
from app import models

load_dotenv()

models.SQLModel.metadata.create_all(engine)

app = FastAPI(title="Workout Tracker API", version="1.0")

# CORS Configuration
origins_env = os.getenv("ALLOWED_ORIGINS", "")
origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

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
app.include_router(sets.router)
