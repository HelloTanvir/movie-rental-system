import tkinter as tk
from tkinter import ttk, messagebox
from auth import AuthenticationApp
from customer import CustomerApp
from models import Staff
from movie import MovieApp
from rental import RentalApp

class MainApp:
    def __init__(self, root, session):
        self.root = root
        self.root.title("Rent a Movie")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.session = session

        self.canvas = None
        self.scrollbar_y = None
        self.scrollbar_x = None
        self.main_frame = None
        self.content_frame = None

        self.staff_member = None

        self.auth_app = AuthenticationApp(self.root, self.session, self.create_scrollable_screen, self.on_login_success)
        self.customer_app = CustomerApp(self.root, self.session, self.create_scrollable_screen)
        self.movie_app = MovieApp(self.root, self.session, self.create_scrollable_screen)
        self.rental_app = RentalApp(self.root, self.session, self.create_scrollable_screen)

    def start(self):
        self.auth_app.show_login_frame()

    def create_scrollable_screen(self):
        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure main frame to expand and fill entire screen
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())

        if self.canvas:
            self.canvas.destroy()

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)

        if self.scrollbar_y:
            self.scrollbar_y.destroy()

        if self.scrollbar_x:
            self.scrollbar_x.destroy()

        self.scrollbar_y = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand = self.scrollbar_y.set, xscrollcommand = self.scrollbar_x.set)

        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.content_frame, anchor='nw')

        # Ensure content frame spans full width of canvas
        self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            width=self.main_frame.winfo_width() - self.scrollbar_y.winfo_width(),
            height=self.main_frame.winfo_height() - self.scrollbar_x.winfo_height(),
        ))

        # Bind mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.canvas.bind_all("<Shift-MouseWheel>", lambda e: self.canvas.xview_scroll(int(-1*(e.delta/120)), "units"))
        
        def _unbind_mousewheel():
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Shift-MouseWheel>")

        self.main_frame.bind("<Destroy>", lambda e: _unbind_mousewheel())

        # reset geometry of the root window
        self.root.geometry("400x500")

        return self.content_frame

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

        # Movie Menu
        movie_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Movie", menu=movie_menu)
        movie_menu.add_command(label="Create Movie", command=self.movie_app.show_create_frame)
        movie_menu.add_separator()
        movie_menu.add_command(label="Show Movies", command=self.movie_app.show_list_frame)

        # Rental Menu
        rental_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Rental", menu=rental_menu)
        rental_menu.add_command(label="Create Rental", command=self.rental_app.show_create_frame)
        rental_menu.add_separator()
        rental_menu.add_command(label="Show Rentals", command=self.rental_app.show_list_frame)
        
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

        self.root.title("Rent a Movie - Dashboard")

        content_frame = self.create_scrollable_screen()
        content_frame.configure(padding=(80, 60))
        
        # Title
        title_label = ttk.Label(content_frame, text="Dashboard", 
                                 font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Welcome message
        welcome_label = ttk.Label(content_frame, text="Welcome to the Rent a Movie!")
        welcome_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Display staff member name
        staff_label = ttk.Label(content_frame, text=f"Logged in as: {staff_member.username}")
        staff_label.grid(row=2, column=0, columnspan=2, pady=5)

