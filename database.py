import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = os.getenv("DB_URL")

if not db_url:
    raise ValueError("DB_URL environment variable is not set")

# Create the SQLALchemy engine
engine = create_engine(db_url)

# SessionLocal --> Create a session (named sessionLocal) class                                    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)