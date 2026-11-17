from app.auth import oauth2
from app.schemas import models, schemas
from app.utils import utils
from app.utils.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    users = db.query(models.UserCreate).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users do not exist"
        )
    return users


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserCreate).filter(models.UserCreate.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user with id {id} found")
    return user


@router.post("/", status_code=201, response_model=schemas.UserResponse)
def create_user(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    user_credentials.password = utils.hash(user_credentials.password)
    new_user = models.UserCreate(**user_credentials.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{id}", response_model=schemas.UserResponse, status_code=200)
def update_user(
    user_credentials: schemas.UserCreate,
    id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.UserCreate).filter(models.UserCreate.id == id)
    user_credentials.password = utils.hash(user_credentials.password)
    if not user.first():
        raise HTTPException(
            status_code=404, detail="Cannot edit user. User doesn't exist"
        )
    user.update(user_credentials.model_dump())  # pyright: ignore[reportArgumentType]
    db.commit()
    return user.first()


@router.delete("/{id}", status_code=204)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserCreate).filter(models.UserCreate.id == id)
    if not user.first():
        raise HTTPException(status_code=404, detail="User not found")
    user.delete(synchronize_session=False)
    db.commit()
