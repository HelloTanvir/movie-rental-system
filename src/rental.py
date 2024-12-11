from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models import Movie, Customer, Rental

class RentalApp:
    def __init__(self, root, session, create_scrollable_screen):
        self.root = root
        self.session = session
        self.create_scrollable_screen = create_scrollable_screen
        self.selected_rental = None
    
    def show_create_frame(self):
        self.root.title("Rent a Movie - Rental Creation")

        content_frame = self.create_scrollable_screen()
        content_frame.configure(padding=(20, 20))

        movies = self.session.query(Movie).all()
        customers = self.session.query(Customer).all()

        # Movie Selection
        movie_label = ttk.Label(content_frame, text="Select Movie:")
        movie_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        movie_combobox = ttk.Combobox(content_frame, width=30)
        movie_combobox['values'] = [movie.name for movie in movies]
        movie_combobox.grid(row=0, column=1, sticky='w', pady=5)

        # Customer Selection
        customer_label = ttk.Label(content_frame, text="Select Customer:")
        customer_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        customer_combobox = ttk.Combobox(content_frame, width=30)
        customer_combobox['values'] = [f"{customer.first_name} {customer.last_name}" for customer in customers]
        customer_combobox.grid(row=1, column=1, sticky='w', pady=5)

        # Due Date
        due_date_label = ttk.Label(content_frame, text="Due Date:")
        due_date_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        due_date_entry = ttk.Entry(content_frame, width=30)
        due_date_entry.grid(row=2, column=1, sticky='w', pady=5)

        form_inputs = {
            "movie": movie_combobox,
            "customer": customer_combobox,
            "due_date": due_date_entry,
        }

        # Submit Button
        submit_button = ttk.Button(content_frame, text="Create Rental", command=lambda: self.create_rental(form_inputs))
        submit_button.grid(row=12, column=0, columnspan=2, pady=20)

    def create_rental(self, form_inputs):
        movie_name = form_inputs["movie"].get()
        customer_name = form_inputs["customer"].get()
        due_date = form_inputs["due_date"].get()

        if not movie_name:
            messagebox.showerror("Error", "Please select a movie")
            return
        
        if not customer_name:
            messagebox.showerror("Error", "Please select a customer")
            return
        
        if not due_date:
            messagebox.showerror("Error", "Please enter a valid due date")
            return

        movie = self.session.query(Movie).filter_by(name=movie_name).first()
        customer = self.session.query(Customer).filter_by(first_name=customer_name.split()[0]).first()

        if not movie:
            messagebox.showerror("Error", "Movie not found")
            return
        
        if not customer:
            messagebox.showerror("Error", "Customer not found")
            return
        
        if movie.available_copies == 0:
            messagebox.showerror("Error", "No available copies of this movie")
            return

        rental = Rental(
            movie_id=movie.id,
            customer_id=customer.id,
            due_date=due_date
        )

        try:
            movie.available_copies -= 1
            self.session.add(rental)
            self.session.commit()            
            messagebox.showinfo("Success", "Rental created successfully")
            # clear form inputs
            for key in form_inputs:
                form_inputs[key].delete(0, tk.END)
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
    def show_list_frame(self):
        self.root.title("Rent a Movie - Rental List")

        content_frame = self.create_scrollable_screen()
        content_frame.configure(padding=(30, 60))

        # override the geometry of the root window
        self.root.geometry("800x600")

        rentals = self.session.query(Rental).all()

        # Title
        title_label = ttk.Label(content_frame, text="Rental List",
                                font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3)

        if rentals:
            # Table
            columns = ("ID", "Movie", "Customer", "Rental Date", "Due Date", "Return Date", "Status")
            tree = ttk.Treeview(content_frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col.capitalize())
            tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select(event, content_frame))
            tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

            # tree should not overflow the frame
            content_frame.columnconfigure(0, weight=1)

            # set column widths
            tree.column("ID", width=50)
            tree.column("Movie", width=150)
            tree.column("Customer", width=150)
            tree.column("Rental Date", width=100)
            tree.column("Due Date", width=100)
            tree.column("Return Date", width=100)
            tree.column("Status", width=100)

            for rental in rentals:
                tree.insert("", "end", values=(
                    rental.id,
                    rental.movie.name,
                    f"{rental.customer.first_name} {rental.customer.last_name}",
                    rental.rental_date,
                    rental.due_date,
                    rental.return_date if rental.return_date else "N/A",
                    rental.rental_status
                ))

            # Scrollbar
            vertical_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
            vertical_scrollbar.grid(row=1, column=2, sticky='ns')
            horizontal_scrollbar = ttk.Scrollbar(content_frame, orient="horizontal", command=tree.xview)
            horizontal_scrollbar.grid(row=2, column=0, columnspan=2, sticky='ew')
            tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        else:
            no_rentals_label = ttk.Label(content_frame, text="No rentals found", padding=10)
            no_rentals_label.grid(row=1, column=0, columnspan=2, pady=10)

    def on_tree_select(self, event, content_frame):
        selected_item = event.widget.selection()[0]
        values = event.widget.item(selected_item, "values")
        self.selected_rental = self.session.query(Rental).get(values[0])

        if self.selected_rental:
            buttons_frame = ttk.Frame(content_frame)
            buttons_frame.grid(row=3, column=0, columnspan=3, pady=10)

            # Returned Button
            return_button = ttk.Button(buttons_frame, text="Return Movie", command=self.return_movie)
            return_button.grid(row=0, column=0, padx=5)

            # Delete Button
            delete_button = ttk.Button(buttons_frame, text="Delete Rental", command=self.delete_rental)
            delete_button.grid(row=0, column=1, padx=5)

            # Overdue Button
            overdue_button = ttk.Button(buttons_frame, text="Mark Overdue", command=self.mark_overdue)
            overdue_button.grid(row=0, column=2, padx=5)

    def return_movie(self):
        if messagebox.askyesno("Return Movie", "Are you sure you want to return this movie?"):
            self.selected_rental.return_date = datetime.now()
            self.selected_rental.rental_status = "returned"
            self.selected_rental.movie.available_copies += 1
            self.session.commit()
            messagebox.showinfo("Success", "Movie returned successfully")
            self.show_list_frame()

    def delete_rental(self):
        if messagebox.askyesno("Delete Rental", "Are you sure you want to delete this rental?"):
            try:
                self.session.delete(self.delete_rental)
                self.session.commit()
                messagebox.showinfo("Success", "Rental deleted successfully")
                self.show_list_frame()
            except Exception as e:
                self.session.rollback()
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def mark_overdue(self):
        if messagebox.askyesno("Mark Overdue", "Are you sure you want to mark this rental as overdue?"):
            self.selected_rental.rental_status = "overdue"
            self.session.commit()
            messagebox.showinfo("Success", "Rental marked as overdue")
            self.show_list_frame()

