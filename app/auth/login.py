from app.auth.oauth2 import create_token
from app.schemas import models
from app.utils import utils
from app.utils.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def login(
    user_credetials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = (db.query(models.UserCreate).filter(models.UserCreate.email == user_credetials.username).first())
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials, please check your email and/or password and try again")
    if not utils.verify(password=user_credetials.password, hash=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials, please check your email and/or password and try again",)
    return {"token": create_token({"user_id": user.id}), "token_type": "bearer"}
