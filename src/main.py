import tkinter as tk
from auth import AuthenticationApp
from config import engine, Session
from models import Base


def main():
    # Create tables
    Base.metadata.create_all(engine)
    
    session = Session()

    root = tk.Tk()
    app = AuthenticationApp(root, session)
    root.mainloop()

    session.close()


main()

