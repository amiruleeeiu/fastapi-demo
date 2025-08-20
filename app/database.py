import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL database
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "demo_fastapi"
DB_USER = "postgres"
DB_PASSWORD = "12345"

# def _ensure_database_exists():
#     """Create the target database if it doesn't exist."""
#     admin_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
#     tmp_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
#     with tmp_engine.connect() as conn:
#         exists = conn.execute(
#             text("SELECT 1 FROM pg_database WHERE datname = :name"),
#             {"name": DB_NAME},
#         ).scalar()
#         if not exists:
#             # Quote the database name to be safe
#             conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
#     tmp_engine.dispose()


# # Ensure DB exists before creating the main engine
# _ensure_database_exists()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,  # 5 minutes
    pool_timeout=20,   # 20 seconds timeout
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:

    try:
        conn=psycopg2.connect(host=DB_HOST,database=DB_NAME,user=DB_USER,password=DB_PASSWORD,cursor_factory=RealDictCursor)

        cursor=conn.cursor()
        print('Database connection was successful.')
        break
    except Exception as error:
        print('Connection to database failed.')
        print(f"Error : {error}")
        time.sleep(2)