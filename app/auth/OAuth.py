import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
TOKEN_EXPIRE_MINUTES = float(os.environ["TOKEN_EXPIRE_MINUTES"])

def create_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})

    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception):
    jwt.decode(token=token, algorithms=ALGORITHM, key=SECRET_KEY)
