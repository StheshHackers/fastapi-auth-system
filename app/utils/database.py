import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = dotenv.find_dotenv()

DB_URL = dotenv.get_key(key_to_get="DB_URL", dotenv_path=env)

engine = create_engine(DB_URL)  # pyright: ignore[reportArgumentType]
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    with SessionLocal() as db:
        yield db
