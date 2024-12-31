from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_USER = 'admin'
DB_PW = '1234'
DB_NAME = 'crud_db'

#URL= f'mysql+mysqlclient://{DB_USER}:{DB_PW}@localhost:3306/{DB_NAME}'
URL= f'mysql+pymysql://{DB_USER}:{DB_PW}@localhost:3306/{DB_NAME}'

engine = create_engine(URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
