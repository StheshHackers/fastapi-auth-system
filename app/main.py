from fastapi import FastAPI

from .auth import login
from .routes import users
from .schemas import models
from .utils.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"health": "OK"}


app.include_router(users.router)
app.include_router(login.router)
