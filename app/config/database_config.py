from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=False, autoflush=False ,bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


