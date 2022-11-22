import sqlalchemy
from sqlalchemy.ext import declarative
import sqlalchemy.orm as orm

SQLALCHAMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@task-tracker-react-postgres/postgres_db"
)

engine = sqlalchemy.create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()
