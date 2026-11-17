import bcrypt


def hash(password: str):
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt()).decode()


def verify(password: str, hash):
    return bcrypt.checkpw(hashed_password=hash.encode(), password=password.encode())
