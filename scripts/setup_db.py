from sqlalchemy import create_engine
from src.config.settings import settings
from src.db.models import Base

def setup():
    print(f"Setting up database at {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    setup()
