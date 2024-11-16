import tkinter as tk
from auth import AuthenticationApp
from config import engine, Session
from models import Base


def main():
    # Test the database connection
    try:
        with engine.connect() as connection:
            print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to database: {e}")

    # Create tables
    Base.metadata.create_all(engine)
    
    session = Session()

    root = tk.Tk()
    app = AuthenticationApp(root, session)
    root.mainloop()

    session.close()


main()

