from config import engine, Session
from models import Base

def main():
    # Create tables
    Base.metadata.create_all(engine)
    
    session = Session()

    # database operations here

    session.close()


main()

