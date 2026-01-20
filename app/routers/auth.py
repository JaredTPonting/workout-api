from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, Session

from ..database import get_session
from ..models import User
from ..auth import verify_password, create_access_token

router = APIRouter(prefix="", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}
