from app.utils.database import Base
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.types import TIMESTAMP


class UserCreate(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
