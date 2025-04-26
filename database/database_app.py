import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .db_settings import settings
from models import Base
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

sync_engine = create_engine(settings.POSTGRES_DATABASE_URLS, echo=True)

engine_a = create_async_engine(settings.POSTGRES_DATABASE_URLA, echo=True)

def create_db_if_not_exists():
    conn = None
    try:
        print(f"{settings.POSTGRES_DB}")
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD
        )
        conn.autocommit = True  
        cursor = conn.cursor()

        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.POSTGRES_DB}'")
        if cursor.fetchone():
            print(f" {settings.POSTGRES_DB} ")
        else:
            cursor.execute(f"CREATE DATABASE \"{settings.POSTGRES_DB}\" ENCODING 'UTF8'")
            print(f"{settings.POSTGRES_DB}")
       
    except psycopg2.Error as e:
        print(f"{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            
def create_tables():

    try:
        engine = create_engine(settings.POSTGRES_DATABASE_URLS, echo=True)
        Base.metadata.create_all(engine) 
        print(f" {settings.POSTGRES_DB} created.")
    except OperationalError as e:
        print(f"{e}")
    except Exception as e:
        print(f"{e}")

async def get_session():
   
    async with AsyncSession(engine_a) as session:
        try:
            yield session
        finally:
            await session.close() 



if __name__ == "__main__":
    create_db_if_not_exists()  
    create_tables()  
