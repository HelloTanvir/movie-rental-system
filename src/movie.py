import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models import Movie

class MovieApp:
    def __init__(self, root, session, create_scrollable_screen):
        self.root = root
        self.session = session
        self.create_scrollable_screen = create_scrollable_screen
        self.selected_movie = None
    
    def show_create_frame(self):
        self.root.title("Movie Rental System - Movie Creation")

        content_frame = self.create_scrollable_screen()
        content_frame.configure(padding=(20, 20))

        # Title
        title_label = ttk.Label(content_frame, text="Create Movie",
                                font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Name
        name_label = ttk.Label(content_frame, text="Name:")
        name_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        name_entry = ttk.Entry(content_frame, width=30)
        name_entry.grid(row=1, column=1, sticky='w', pady=5)

        # Description
        description_label = ttk.Label(content_frame, text="Description:")
        description_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        description_entry = tk.Text(content_frame, width=30, height=5)
        description_entry.grid(row=2, column=1, sticky='w', pady=5)

        # Release Year
        release_year_label = ttk.Label(content_frame, text="Release Year:")
        release_year_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        release_year_entry = ttk.Entry(content_frame, width=30)
        release_year_entry.grid(row=3, column=1, sticky='w', pady=5)

        # Rental Rate
        rental_rate_label = ttk.Label(content_frame, text="Rental Rate:")
        rental_rate_label.grid(row=4, column=0, sticky=tk.W, pady=5)

        rental_rate_entry = ttk.Entry(content_frame, width=30)
        rental_rate_entry.grid(row=4, column=1, sticky='w', pady=5)

        # Duration
        duration_label = ttk.Label(content_frame, text="Duration (mins):")
        duration_label.grid(row=5, column=0, sticky=tk.W, pady=5)

        duration_entry = ttk.Entry(content_frame, width=30)
        duration_entry.grid(row=5, column=1, sticky='w', pady=5)

        # Genre
        genre_label = ttk.Label(content_frame, text="Genre:")
        genre_label.grid(row=6, column=0, sticky=tk.W, pady=5)

        genre_entry = ttk.Entry(content_frame, width=30)
        genre_entry.grid(row=6, column=1, sticky='w', pady=5)

        # Rating
        rating_label = ttk.Label(content_frame, text="Rating:")
        rating_label.grid(row=7, column=0, sticky=tk.W, pady=5)

        rating_entry = ttk.Entry(content_frame, width=30)
        rating_entry.grid(row=7, column=1, sticky='w', pady=5)

        # Director
        director_label = ttk.Label(content_frame, text="Director:")
        director_label.grid(row=8, column=0, sticky=tk.W, pady=5)

        director_entry = ttk.Entry(content_frame, width=30)
        director_entry.grid(row=8, column=1, sticky='w', pady=5)

        # Image
        image_label = ttk.Label(content_frame, text="Image:")
        image_label.grid(row=9, column=0, sticky=tk.W, pady=5)

        image_entry = ttk.Entry(content_frame, width=30)
        image_entry.grid(row=9, column=1, sticky='w', pady=5)

        # Total Copies
        total_copies_label = ttk.Label(content_frame, text="Total Copies:")
        total_copies_label.grid(row=10, column=0, sticky=tk.W, pady=5)

        total_copies_entry = ttk.Entry(content_frame, width=30)
        total_copies_entry.grid(row=10, column=1, sticky='w', pady=5)

        form_inputs = {
            "name": name_entry,
            "description": description_entry,
            "release_year": release_year_entry,
            "rental_rate": rental_rate_entry,
            "duration": duration_entry,
            "genre": genre_entry,
            "rating": rating_entry,
            "director": director_entry,
            "image": image_entry,
            "total_copies": total_copies_entry,
        }

        # Submit Button
        submit_button = ttk.Button(content_frame, text="Create Movie", command=lambda: self.create_movie(form_inputs))
        submit_button.grid(row=12, column=0, columnspan=2, pady=20)

    def create_movie(self, form_inputs):
        movie = Movie(
            name=form_inputs["name"].get(),
            description=form_inputs["description"].get("1.0", tk.END),
            release_year=form_inputs["release_year"].get(),
            rental_rate=form_inputs["rental_rate"].get(),
            duration_mins=form_inputs["duration"].get(),
            genre=form_inputs["genre"].get(),
            rating=form_inputs["rating"].get(),
            director=form_inputs["director"].get(),
            image=form_inputs["image"].get(),
            total_copies=form_inputs["total_copies"].get(),
            available_copies=form_inputs["total_copies"].get() # initially all copies are available
        )

        try:
            self.session.add(movie)
            self.session.commit()
            messagebox.showinfo("Success", "Movie created successfully")
            # clear form inputs
            for key in form_inputs:
                form_inputs[key].delete(0, tk.END)
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
    def show_list_frame(self):
        self.root.title("Movie Rental System - Movie List")

        content_frame = self.create_scrollable_screen()
        content_frame.configure(padding=(30, 60))

        # override the geometry of the root window
        self.root.geometry("800x600")

        movies = self.session.query(Movie).all()

        # Title
        title_label = ttk.Label(content_frame, text="Movie List",
                                font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2)

        if movies:
            # Table
            columns = ("ID", "Title", "Release Year", "Genre", "Director", "Rating", "Total Copies", "Available Copies")
            tree = ttk.Treeview(content_frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col.capitalize())
            tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select(event, content_frame))
            tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

            # tree should not overflow the frame
            content_frame.columnconfigure(0, weight=1)

            # set column widths
            tree.column("ID", width=50)
            tree.column("Title", width=200)
            tree.column("Release Year", width=100)
            tree.column("Genre", width=100)
            tree.column("Director", width=100)
            tree.column("Rating", width=50)
            tree.column("Total Copies", width=50)
            tree.column("Available Copies", width=50)

            for movie in movies:
                tree.insert("", "end", values=(
                    movie.id,
                    movie.name,
                    movie.release_year,
                    movie.genre,
                    movie.director,
                    movie.rating,
                    movie.total_copies,
                    movie.available_copies
                ))

            # Scrollbar
            vertical_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
            vertical_scrollbar.grid(row=1, column=2, sticky='ns')
            horizontal_scrollbar = ttk.Scrollbar(content_frame, orient="horizontal", command=tree.xview)
            horizontal_scrollbar.grid(row=2, column=0, columnspan=2, sticky='ew')
            tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        else:
            no_movies_label = ttk.Label(content_frame, text="No movies found", padding=10)
            no_movies_label.grid(row=1, column=0, columnspan=2, pady=10)

    def on_tree_select(self, event, content_frame):
        selected_item = event.widget.selection()[0]
        values = event.widget.item(selected_item, "values")
        self.selected_movie = self.session.query(Movie).get(values[0])

        if self.selected_movie:
            # Delete Button
            delete_button = ttk.Button(content_frame, text="Delete", command=self.delete_movie)
            delete_button.grid(row=3, column=0, pady=10)

            # Update Button
            update_button = ttk.Button(content_frame, text="Update", command=self.show_update_frame)
            update_button.grid(row=3, column=1, pady=10)

    def delete_movie(self):
        if messagebox.askyesno("Delete Movie", "Are you sure you want to delete this movie?"):
            try:
                self.session.delete(self.selected_movie)
                self.session.commit()
                messagebox.showinfo("Success", "Movie deleted successfully")
                self.show_list_frame()
            except Exception as e:
                self.session.rollback()
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_update_frame(self):
        self.root.title("Movie Rental System - Update Movie")

        content_frame = self.create_scrollable_screen()
        content_frame.configure(padding=(20, 20))

        # Title
        title_label = ttk.Label(content_frame, text="Update Movie",
                                font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Name
        name_label = ttk.Label(content_frame, text="Name:")
        name_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        name_entry = ttk.Entry(content_frame, width=30)
        name_entry.insert(0, self.selected_movie.name)
        name_entry.grid(row=1, column=1, sticky='w', pady=5)

        # Description
        description_label = ttk.Label(content_frame, text="Description:")
        description_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        description_entry = tk.Text(content_frame, width=30, height=5)
        description_entry.insert(tk.END, self.selected_movie.description)
        description_entry.grid(row=2, column=1, sticky='w', pady=5)

        # Release Year
        release_year_label = ttk.Label(content_frame, text="Release Year:")
        release_year_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        release_year_entry = ttk.Entry(content_frame, width=30)
        release_year_entry.insert(0, self.selected_movie.release_year)
        release_year_entry.grid(row=3, column=1, sticky='w', pady=5)

        # Rental Rate
        rental_rate_label = ttk.Label(content_frame, text="Rental Rate:")
        rental_rate_label.grid(row=4, column=0, sticky=tk.W, pady=5)

        rental_rate_entry = ttk.Entry(content_frame, width=30)
        rental_rate_entry.insert(0, self.selected_movie.rental_rate)
        rental_rate_entry.grid(row=4, column=1, sticky='w', pady=5)

        # Duration
        duration_label = ttk.Label(content_frame, text="Duration (mins):")
        duration_label.grid(row=5, column=0, sticky=tk.W, pady=5)

        duration_entry = ttk.Entry(content_frame, width=30)
        duration_entry.insert(0, self.selected_movie.duration_mins)
        duration_entry.grid(row=5, column=1, sticky='w', pady=5)

        # Genre
        genre_label = ttk.Label(content_frame, text="Genre:")
        genre_label.grid(row=6, column=0, sticky=tk.W, pady=5)

        genre_entry = ttk.Entry(content_frame, width=30)
        genre_entry.insert(0, self.selected_movie.genre)
        genre_entry.grid(row=6, column=1, sticky='w', pady=5)

        # Rating
        rating_label = ttk.Label(content_frame, text="Rating:")
        rating_label.grid(row=7, column=0, sticky=tk.W, pady=5)

        rating_entry = ttk.Entry(content_frame, width=30)
        rating_entry.insert(0, self.selected_movie.rating)
        rating_entry.grid(row=7, column=1, sticky='w', pady=5)

        # Director
        director_label = ttk.Label(content_frame, text="Director:")
        director_label.grid(row=8, column=0, sticky=tk.W, pady=5)

        director_entry = ttk.Entry(content_frame, width=30)
        director_entry.insert(0, self.selected_movie.director)
        director_entry.grid(row=8, column=1, sticky='w', pady=5)

        # Image
        image_label = ttk.Label(content_frame, text="Image:")
        image_label.grid(row=9, column=0, sticky=tk.W, pady=5)

        image_entry = ttk.Entry(content_frame, width=30)
        image_entry.insert(0, self.selected_movie.image)
        image_entry.grid(row=9, column=1, sticky='w', pady=5)

        # Total Copies
        total_copies_label = ttk.Label(content_frame, text="Total Copies:")
        total_copies_label.grid(row=10, column=0, sticky=tk.W, pady=5)

        total_copies_entry = ttk.Entry(content_frame, width=30)
        total_copies_entry.insert(0, self.selected_movie.total_copies)
        total_copies_entry.grid(row=10, column=1, sticky='w', pady=5)

        form_inputs = {
            "name": name_entry,
            "description": description_entry,
            "release_year": release_year_entry,
            "rental_rate": rental_rate_entry,
            "duration": duration_entry,
            "genre": genre_entry,
            "rating": rating_entry,
            "director": director_entry,
            "image": image_entry,
            "total_copies": total_copies_entry,
        }

        # Submit Button
        submit_button = ttk.Button(content_frame, text="Update Movie", command=lambda: self.update_movie(form_inputs))
        submit_button.grid(row=12, column=0, columnspan=2, pady=20)

    def update_movie(self, form_inputs):
        self.selected_movie.name = form_inputs["name"].get()
        self.selected_movie.description = form_inputs["description"].get("1.0", tk.END)
        self.selected_movie.release_year = form_inputs["release_year"].get()
        self.selected_movie.rental_rate = form_inputs["rental_rate"].get()
        self.selected_movie.duration_mins = form_inputs["duration"].get()
        self.selected_movie.genre = form_inputs["genre"].get()
        self.selected_movie.rating = form_inputs["rating"].get()
        self.selected_movie.director = form_inputs["director"].get()
        self.selected_movie.image = form_inputs["image"].get()
        self.selected_movie.total_copies = form_inputs["total_copies"].get()

        try:
            self.session.commit()
            messagebox.showinfo("Success", "Movie updated successfully")
            self.show_list_frame()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

