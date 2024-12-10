import tkinter as tk
from tkinter import ttk, messagebox
from auth import AuthenticationApp
from customer import CustomerApp
from models import Staff

class MainApp:
    def __init__(self, root, session):
        self.root = root
        self.root.title("Movie Rental System")
        self.root.geometry("400x500")
        
        self.session = session

        self.main_frame = None

        self.staff_member = None

        self.auth_app = AuthenticationApp(self.root, self.session, self.get_main_frame, self.on_login_success)
        self.customer_app = CustomerApp(self.root, self.session, self.get_main_frame)

    def start(self):
        self.auth_app.show_login_frame()

    def get_main_frame(self):
        if self.main_frame:
            # clear the main frame
            for widget in self.main_frame.winfo_children():
                widget.destroy()
        else:
            self.main_frame = ttk.Frame(self.root, padding="20")
            self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # reset geometry of the root window
        self.root.geometry("400x500")

        return self.main_frame

    def on_login_success(self, staff_member):
        self.create_menu_bar()
        self.show_dashboard(staff_member)

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Action Menu
        action_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Action", menu=action_menu)
        action_menu.add_command(label="Dashboard", command=lambda: self.show_dashboard(self.staff_member))
        action_menu.add_separator()
        action_menu.add_command(label="Logout", command=self.logout)
        action_menu.add_separator()
        action_menu.add_command(label="Exit", command=self.root.quit)
        
        # Customer Menu
        customer_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Customer", menu=customer_menu)
        customer_menu.add_command(label="Create Customer", command=self.customer_app.show_create_frame)
        customer_menu.add_separator()
        customer_menu.add_command(label="Show Customers", command=self.customer_app.show_list_frame)
        
        # Reports Menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Revenue Report")
        reports_menu.add_separator()
        reports_menu.add_command(label="Popular Movies")
        reports_menu.add_separator()
        reports_menu.add_command(label="Late Returns")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # clear the menu bar
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Menu):
                    widget.destroy()

            self.auth_app.show_login_frame()
    
    def show_dashboard(self, staff_member: Staff):
        self.staff_member = staff_member

        self.root.title("Movie Rental System - Dashboard")

        self.main_frame = self.get_main_frame()

        if not self.main_frame:
            self.main_frame = ttk.Frame(self.root, padding="20")
            self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Dashboard", 
                                 font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Welcome message
        welcome_label = ttk.Label(self.main_frame, text="Welcome to the Movie Rental System!")
        welcome_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Display staff member name
        staff_label = ttk.Label(self.main_frame, text=f"Logged in as: {staff_member.username}")
        staff_label.grid(row=2, column=0, columnspan=2, pady=5)

