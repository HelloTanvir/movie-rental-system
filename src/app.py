import tkinter as tk
from tkinter import ttk, messagebox
from auth import AuthenticationFrame
from models import Staff

class MainApplication:
    def __init__(self, root, session):
        self.root = root
        self.root.title("Movie Rental System")
        self.root.geometry("800x600")
        
        self.session = session

        self.main_content = None

        # Start with login screen
        self.show_login()

    def show_login(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.login_frame = AuthenticationFrame(self.root, self.session, self.on_login_success)

    def on_login_success(self, staff_member):
        # Clear login frame
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.create_menu_bar()
        
        self.show_dashboard(staff_member)

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Management Menu
        management_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Management", menu=management_menu)
        management_menu.add_command(label="Customers", command=self.show_customer_management)
        management_menu.add_command(label="Movies", command=self.show_movie_management)
        management_menu.add_command(label="Rentals", command=self.show_rental_management)
        
        # Reports Menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Revenue Report")
        reports_menu.add_command(label="Popular Movies")
        reports_menu.add_command(label="Late Returns")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.show_login()
    
    def show_dashboard(self, staff_member: Staff):
        self.root.title("Movie Rental System - Dashboard")

        # Main content area
        self.main_content = ttk.Frame(self.root, padding="20")
        self.main_content.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(self.main_content, text="Dashboard", 
                                 font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Welcome message
        welcome_label = ttk.Label(self.main_content, text="Welcome to the Movie Rental System!")
        welcome_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Display staff member name
        staff_label = ttk.Label(self.main_content, text=f"Logged in as: {staff_member.username}")
        staff_label.grid(row=2, column=0, columnspan=2, pady=5)

    def show_customer_management(self):
        self.root.title("Movie Rental System - Customer Management")

        # Clear main content area
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()
        
        # Initialize customer management
        # CustomerManagement(self.root, self.session)

    def show_movie_management(self):
        self.root.title("Movie Rental System - Movie Management")
        messagebox.showinfo("Info", "Movie Management - Coming Soon!")

    def show_rental_management(self):
        self.root.title("Movie Rental System - Rental Management")
        messagebox.showinfo("Info", "Rental Management - Coming Soon!")

