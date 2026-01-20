import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

from dotenv import load_dotenv

from app.routers import exercises, workouts, sets, auth
from app.database import engine, get_session
from app import models
from app.auth import hash_password

load_dotenv()

models.SQLModel.metadata.create_all(engine)

# Create initial user if INIT_USERNAME and INIT_PASSWORD are set
init_username = os.getenv("INIT_USERNAME")
init_password = os.getenv("INIT_PASSWORD")

if init_username and init_password:
    db = next(get_session())
    existing_user = db.exec(select(models.User).where(models.User.username == init_username)).first()
    if not existing_user:
        user = models.User(
            username=init_username,
            hashed_password=hash_password(init_password),
        )
        db.add(user)
        db.commit()
        print(f"Initial user '{init_username}' created.")
    else:
        print(f"User '{init_username}' already exists, skipping creation.")
    db.close()

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
app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(workouts.router)
app.include_router(sets.router)
