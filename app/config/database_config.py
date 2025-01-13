from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import Settings

settings = Settings()
database_url = f'postgresql://{settings.pg_username}:{settings.pg_password}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db_name}'
engine = create_engine(database_url, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


