from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Define your database URL using postgres
db_url="postgresql://postgres:Abhishek%40123@localhost:5432/mydatabase"

# Create the SQLALchemy engine
engine = create_engine(db_url)     

# SessionLocal --> Create a session (named sessionLocal) class                                    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


