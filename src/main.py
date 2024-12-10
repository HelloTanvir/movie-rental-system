import tkinter as tk
from app import MainApp
from config import engine, Session
from models import Base


def main():
    try:
        with engine.connect() as connection:
            print("Database connection successful!", connection)
    except Exception as e:
        print(f"Error connecting to database: {e}")

    # Create tables
    Base.metadata.create_all(engine)
    
    session = Session()

    root = tk.Tk()
    app = MainApp(root, session)
    app.start()
    root.mainloop()

    session.close()


main()

