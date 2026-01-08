from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the SQLALchemy engine
engine = create_engine(db_url)     

# SessionLocal --> Create a session (named sessionLocal) class                                    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


