from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from settings import DATABASE_URL

try:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("Database created successfully")
except OperationalError as e:
    print(f"Failed to connect to database: {e}")
