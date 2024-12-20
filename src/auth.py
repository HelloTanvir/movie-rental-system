import tkinter as tk
from tkinter import ttk, messagebox
from models import Staff
from datetime import datetime
import bcrypt
import re

class AuthenticationApp:
    def __init__(self, root, session, create_scrollable_screen, login_callback):
        self.root = root
        self.session = session
        self.create_scrollable_screen = create_scrollable_screen
        self.login_callback = login_callback
            
    def show_login_frame(self):
        self.root.title("Rent a Movie - Staff Login")

        content_frame = self.create_scrollable_screen()
        content_frame.configure(padding=(100, 50))
        
        # Title
        title_label = ttk.Label(content_frame, text="Rent a Movie", 
                              font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)
        
        # Username
        ttk.Label(content_frame, text="Username:").grid(row=1, column=0, 
                                                         sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(content_frame, textvariable=self.username_var)
        self.username_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Password
        ttk.Label(content_frame, text="Password:").grid(row=3, column=0, 
                                                         sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(content_frame, textvariable=self.password_var, 
                                      show="*")
        self.password_entry.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Login Button
        login_btn = ttk.Button(content_frame, text="Login", command=self.login)
        login_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Register Link
        register_link = ttk.Button(content_frame, text="Register New Staff", 
                                 command=self.show_register_frame)
        register_link.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Configure grid weights
        content_frame.columnconfigure(0, weight=1)
        
    def show_register_frame(self):
        self.root.title("Rent a Movie - Register New Staff")

        content_frame = self.create_scrollable_screen()
        content_frame.configure(padding=(80, 40))
        
        # Title
        title_label = ttk.Label(content_frame, text="Register New Staff", 
                              font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Username
        ttk.Label(content_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_username_var = tk.StringVar()
        self.reg_username_entry = ttk.Entry(content_frame, textvariable=self.reg_username_var)
        self.reg_username_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Email
        ttk.Label(content_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_email_var = tk.StringVar()
        self.reg_email_entry = ttk.Entry(content_frame, textvariable=self.reg_email_var)
        self.reg_email_entry.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Password
        ttk.Label(content_frame, text="Password:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.reg_password_var = tk.StringVar()
        self.reg_password_entry = ttk.Entry(content_frame, textvariable=self.reg_password_var, 
                                          show="*")
        self.reg_password_entry.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Confirm Password
        ttk.Label(content_frame, text="Confirm Password:").grid(row=7, column=0, 
                                                                 sticky=tk.W, pady=5)
        self.reg_confirm_var = tk.StringVar()
        self.reg_confirm_entry = ttk.Entry(content_frame, textvariable=self.reg_confirm_var, 
                                         show="*")
        self.reg_confirm_entry.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Register Button
        register_btn = ttk.Button(content_frame, text="Register", command=self.register)
        register_btn.grid(row=9, column=0, columnspan=2, pady=20)
        
        # Back to Login Link
        back_link = ttk.Button(content_frame, text="Back to Login", 
                             command=self.show_login_frame)
        back_link.grid(row=10, column=0, columnspan=2, pady=5)
    
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        # At least 8 characters, 1 uppercase, 1 lowercase, 1 number
        if (len(password) < 8 or not re.search(r'[A-Z]', password) or 
            not re.search(r'[a-z]', password) or not re.search(r'\d', password)):
            return False
        return True
    
    def register(self):
        username = self.reg_username_var.get().strip()
        email = self.reg_email_var.get().strip()
        password = self.reg_password_var.get()
        confirm_password = self.reg_confirm_var.get()
        
        # Validation
        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return
        
        if not self.validate_password(password):
            messagebox.showerror("Error", 
                               "Password must be at least 8 characters long and contain uppercase, "
                               "lowercase, and numbers!")
            return
        
        # Check if username or email already exists
        if self.session.query(Staff).filter_by(username=username).first():
            messagebox.showerror("Error", "Username already exists!")
            return
        
        if self.session.query(Staff).filter_by(email=email).first():
            messagebox.showerror("Error", "Email already exists!")
            return
        
        # Create new staff member
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_staff = Staff(
            username=username,
            email=email,
            password_hash=password_hash.decode('utf-8')
        )
        
        try:
            self.session.add(new_staff)
            self.session.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_frame()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
        
        staff = self.session.query(Staff).filter_by(username=username).first()
        
        if staff and bcrypt.checkpw(password.encode('utf-8'), 
                                  staff.password_hash.encode('utf-8')):
            # Update last login
            staff.last_login = datetime.now()
            self.session.commit()
            
            messagebox.showinfo("Success", "Login successful!")
            
            self.login_callback(staff)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

