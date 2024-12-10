import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models import Customer

class CustomerApp:
    def __init__(self, root, session, get_main_frame):
        self.root = root
        self.session = session
        self.get_main_frame = get_main_frame
        self.selected_customer = None
    
    def show_create_frame(self):
        self.root.title("Movie Rental System - Customer Registration")

        main_frame = self.get_main_frame()

        # Title
        title_label = ttk.Label(main_frame, text="Customer Registration",
                                font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # First Name
        first_name_label = ttk.Label(main_frame, text="First Name:")
        first_name_label.grid(row=1, column=0, sticky='w', pady=5)

        first_name_entry = ttk.Entry(main_frame, width=30)
        first_name_entry.grid(row=1, column=1, sticky='w')

        # Last Name
        last_name_label = ttk.Label(main_frame, text="Last Name:")
        last_name_label.grid(row=2, column=0, sticky='w', pady=5)

        last_name_entry = ttk.Entry(main_frame, width=30)
        last_name_entry.grid(row=2, column=1, sticky='w')

        # Email
        email_label = ttk.Label(main_frame, text="Email:")
        email_label.grid(row=3, column=0, sticky='w', pady=5)

        email_entry = ttk.Entry(main_frame, width=30)
        email_entry.grid(row=3, column=1, sticky='w')

        # Phone
        phone_label = ttk.Label(main_frame, text="Phone:")
        phone_label.grid(row=4, column=0, sticky='w', pady=5)

        phone_entry = ttk.Entry(main_frame, width=30)
        phone_entry.grid(row=4, column=1, sticky='w')

        # Address
        address_label = ttk.Label(main_frame, text="Address:")
        address_label.grid(row=5, column=0, sticky='w', pady=5)

        address_entry = tk.Entry(main_frame, width=30)
        address_entry.grid(row=5, column=1, sticky='w')

        form_inputs = {
            'first_name': first_name_entry,
            'last_name': last_name_entry,
            'email': email_entry,
            'phone': phone_entry,
            'address': address_entry
        }

        # Submit Button
        submit_button = ttk.Button(main_frame, text="Register Customer", command=lambda: self.register_customer(form_inputs))
        submit_button.grid(row=6, column=0, columnspan=2, pady=20)

    def register_customer(self, form_inputs):
        customer = Customer(
            first_name=form_inputs['first_name'].get(),
            last_name=form_inputs['last_name'].get(),
            email=form_inputs['email'].get(),
            phone=form_inputs['phone'].get(),
            address=form_inputs['address'].get()
        )

        if self.session.query(Customer).filter_by(email=customer.email).first():
            messagebox.showerror("Error", "Customer with that email already exists")
            return

        try:
            self.session.add(customer)
            self.session.commit()
            messagebox.showinfo("Success", "Customer registered successfully")
            # clear form inputs
            for key in form_inputs:
                form_inputs[key].delete(0, tk.END)
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
    def show_list_frame(self):
        self.root.title("Movie Rental System - Customer List")

        main_frame = self.get_main_frame()

        # override the geometry of the root window
        self.root.geometry("800x600")

        customers = self.session.query(Customer).all()

        # Title
        title_label = ttk.Label(main_frame, text="Customer List",
                                font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        if customers:
            # Table
            columns = ("ID", "Name", "Email", "Phone", "Address")
            tree = ttk.Treeview(main_frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col.capitalize())
            tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select(event, main_frame))
            tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

            # tree should not overflow the frame
            main_frame.columnconfigure(0, weight=1)

            # set column widths
            tree.column("ID", width=50)
            tree.column("Name", width=200)
            tree.column("Email", width=100)
            tree.column("Phone", width=100)
            tree.column("Address", width=200)

            for customer in customers:
                tree.insert("", "end", values=(
                    customer.id,
                    f"{customer.first_name} {customer.last_name}",
                    customer.email,
                    customer.phone,
                    customer.address
                ))

            # Scrollbar
            vertical_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
            vertical_scrollbar.grid(row=1, column=2, sticky='ns')
            horizontal_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=tree.xview)
            horizontal_scrollbar.grid(row=2, column=0, columnspan=2, sticky='ew')
            tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        else:
            no_customers_label = ttk.Label(main_frame, text="No customers found", padding=10)
            no_customers_label.grid(row=1, column=0, columnspan=2, pady=10)

    def on_tree_select(self, event, main_frame):
        selected_item = event.widget.selection()[0]
        values = event.widget.item(selected_item, "values")
        self.selected_customer = self.session.query(Customer).get(values[0])

        if self.selected_customer:
            # Delete Button
            delete_button = ttk.Button(main_frame, text="Delete", command=self.delete_customer)
            delete_button.grid(row=3, column=0, pady=10)

            # Update Button
            update_button = ttk.Button(main_frame, text="Update", command=self.show_update_frame)
            update_button.grid(row=3, column=1, pady=10)

    def delete_customer(self):
        if messagebox.askyesno("Delete Customer", "Are you sure you want to delete this customer?"):
            try:
                self.session.delete(self.selected_customer)
                self.session.commit()
                messagebox.showinfo("Success", "Customer deleted successfully")
                self.show_list_frame()
            except Exception as e:
                self.session.rollback()
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_update_frame(self):
        self.root.title("Movie Rental System - Update Customer")

        main_frame = self.get_main_frame()

        # Title
        title_label = ttk.Label(main_frame, text="Update Customer",
                                font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # First Name
        first_name_label = ttk.Label(main_frame, text="First Name:")
        first_name_label.grid(row=1, column=0, sticky='w', pady=5)

        first_name_entry = ttk.Entry(main_frame, width=30)
        first_name_entry.insert(0, self.selected_customer.first_name)
        first_name_entry.grid(row=1, column=1, sticky='w')

        # Last Name
        last_name_label = ttk.Label(main_frame, text="Last Name:")
        last_name_label.grid(row=2, column=0, sticky='w', pady=5)

        last_name_entry = ttk.Entry(main_frame, width=30)
        last_name_entry.insert(0, self.selected_customer.last_name)
        last_name_entry.grid(row=2, column=1, sticky='w')

        # Email
        email_label = ttk.Label(main_frame, text="Email:")
        email_label.grid(row=3, column=0, sticky='w', pady=5)

        email_entry = ttk.Entry(main_frame, width=30)
        email_entry.insert(0, self.selected_customer.email)
        email_entry.grid(row=3, column=1, sticky='w')

        # Phone
        phone_label = ttk.Label(main_frame, text="Phone:")
        phone_label.grid(row=4, column=0, sticky='w', pady=5)

        phone_entry = ttk.Entry(main_frame, width=30)
        phone_entry.insert(0, self.selected_customer.phone)
        phone_entry.grid(row=4, column=1, sticky='w')

        # Address
        address_label = ttk.Label(main_frame, text="Address:")
        address_label.grid(row=5, column=0, sticky='w', pady=5)

        address_entry = tk.Entry(main_frame, width=30)
        address_entry.insert(0, self.selected_customer.address)
        address_entry.grid(row=5, column=1, sticky='w')

        form_inputs = {
            'first_name': first_name_entry,
            'last_name': last_name_entry,
            'email': email_entry,
            'phone': phone_entry,
            'address': address_entry
        }

        # Submit Button
        submit_button = ttk.Button(main_frame, text="Update Customer", command=lambda: self.update_customer(form_inputs))
        submit_button.grid(row=6, column=0, columnspan=2, pady=20)

    def update_customer(self, form_inputs):
        self.selected_customer.first_name = form_inputs['first_name'].get()
        self.selected_customer.last_name = form_inputs['last_name'].get()
        self.selected_customer.email = form_inputs['email'].get()
        self.selected_customer.phone = form_inputs['phone'].get()
        self.selected_customer.address = form_inputs['address'].get()

        try:
            self.session.commit()
            messagebox.showinfo("Success", "Customer updated successfully")
            self.show_list_frame()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

