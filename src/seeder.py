from datetime import datetime
from config import engine, Session
from models import Base, Customer, Movie


def seed_database():
    try:
        with engine.connect() as connection:
            print("Database connection successful!", connection)
    except Exception as e:
        print(f"Error connecting to database: {e}")

    # Create tables
    Base.metadata.create_all(engine)
    
    session = Session()

    movies_data = [
        {"name": "Inception", "release_year": 2010, "rental_rate": 4.99, "duration_mins": 148, "genre": "Sci-Fi", "director": "Christopher Nolan", "total_copies": 10, "available_copies": 10, "rating": 8.8},
        {"name": "Parasite", "release_year": 2019, "rental_rate": 4.50, "duration_mins": 132, "genre": "Drama", "director": "Bong Joon-ho", "total_copies": 8, "available_copies": 8, "rating": 8.6},
        {"name": "The Shawshank Redemption", "release_year": 1994, "rental_rate": 3.99, "duration_mins": 142, "genre": "Drama", "director": "Frank Darabont", "total_copies": 12, "available_copies": 12, "rating": 9.3},
        {"name": "Interstellar", "release_year": 2014, "rental_rate": 5.49, "duration_mins": 169, "genre": "Sci-Fi", "director": "Christopher Nolan", "total_copies": 9, "available_copies": 9, "rating": 8.6},
        {"name": "Amélie", "release_year": 2001, "rental_rate": 4.25, "duration_mins": 122, "genre": "Romance", "director": "Jean-Pierre Jeunet", "total_copies": 7, "available_copies": 7, "rating": 8.3},
        
        {"name": "Aynabaji", "release_year": 2016, "rental_rate": 3.50, "duration_mins": 135, "genre": "Drama", "director": "Amitabh Reza Chowdhury", "total_copies": 6, "available_copies": 6, "rating": 7.8},
        {"name": "Ghare Baire", "release_year": 2015, "rental_rate": 3.75, "duration_mins": 128, "genre": "Drama", "director": "Aparna Sen", "total_copies": 5, "available_copies": 5, "rating": 7.5},
        {"name": "Monpura", "release_year": 2009, "rental_rate": 3.25, "duration_mins": 140, "genre": "Romance", "director": "Giasuddin Selim", "total_copies": 7, "available_copies": 7, "rating": 8.0},
        {"name": "Made in Bangladesh", "release_year": 2019, "rental_rate": 4.00, "duration_mins": 95, "genre": "Social Drama", "director": "Rubaiyat Hossain", "total_copies": 4, "available_copies": 4, "rating": 7.2},
        {"name": "Television", "release_year": 2012, "rental_rate": 3.50, "duration_mins": 110, "genre": "Drama", "director": "Mostofa Sarwar Farooki", "total_copies": 6, "available_copies": 6, "rating": 7.6},
        
        {"name": "The Matrix", "release_year": 1999, "rental_rate": 4.75, "duration_mins": 136, "genre": "Sci-Fi", "director": "Lana Wachowski", "total_copies": 11, "available_copies": 11, "rating": 8.7},
        {"name": "Spirited Away", "release_year": 2001, "rental_rate": 4.25, "duration_mins": 125, "genre": "Animation", "director": "Hayao Miyazaki", "total_copies": 8, "available_copies": 8, "rating": 8.6},
        {"name": "Pulp Fiction", "release_year": 1994, "rental_rate": 4.50, "duration_mins": 154, "genre": "Crime", "director": "Quentin Tarantino", "total_copies": 9, "available_copies": 9, "rating": 8.9},
        {"name": "The Dark Knight", "release_year": 2008, "rental_rate": 5.25, "duration_mins": 152, "genre": "Action", "director": "Christopher Nolan", "total_copies": 10, "available_copies": 10, "rating": 9.0},
        {"name": "Roma", "release_year": 2018, "rental_rate": 4.00, "duration_mins": 135, "genre": "Drama", "director": "Alfonso Cuarón", "total_copies": 5, "available_copies": 5, "rating": 8.2},
        
        {"name": "Third Person Singular Number", "release_year": 2016, "rental_rate": 3.75, "duration_mins": 118, "genre": "Drama", "director": "Rifat Arefin Shuvo", "total_copies": 5, "available_copies": 5, "rating": 7.4},
        {"name": "Oggatonama", "release_year": 2013, "rental_rate": 3.25, "duration_mins": 105, "genre": "Drama", "director": "Amitabh Reza Chowdhury", "total_copies": 4, "available_copies": 4, "rating": 7.1},
        {"name": "No Dorai", "release_year": 2014, "rental_rate": 3.50, "duration_mins": 124, "genre": "Comedy", "director": "Mostofa Sarwar Farooki", "total_copies": 6, "available_copies": 6, "rating": 7.5},
        {"name": "Joyjatra", "release_year": 2004, "rental_rate": 3.00, "duration_mins": 130, "genre": "Drama", "director": "Humayun Ahmed", "total_copies": 5, "available_copies": 5, "rating": 7.3},
        {"name": "Ant Story", "release_year": 2017, "rental_rate": 3.75, "duration_mins": 110, "genre": "Drama", "director": "Nuhash Humayun", "total_copies": 4, "available_copies": 4, "rating": 7.0},
        
        {"name": "Pan's Labyrinth", "release_year": 2006, "rental_rate": 4.25, "duration_mins": 118, "genre": "Fantasy", "director": "Guillermo del Toro", "total_copies": 7, "available_copies": 7, "rating": 8.2},
        {"name": "The Social Network", "release_year": 2010, "rental_rate": 4.50, "duration_mins": 120, "genre": "Biography", "director": "David Fincher", "total_copies": 8, "available_copies": 8, "rating": 7.7},
        {"name": "Memories of Murder", "release_year": 2003, "rental_rate": 4.00, "duration_mins": 132, "genre": "Crime", "director": "Bong Joon-ho", "total_copies": 6, "available_copies": 6, "rating": 8.1},
        {"name": "City of God", "release_year": 2002, "rental_rate": 4.25, "duration_mins": 130, "genre": "Crime", "director": "Fernando Meirelles", "total_copies": 7, "available_copies": 7, "rating": 8.6},
        {"name": "Your Name", "release_year": 2016, "rental_rate": 4.50, "duration_mins": 107, "genre": "Animation", "director": "Makoto Shinkai", "total_copies": 5, "available_copies": 5, "rating": 8.4},
        
        {"name": "Ghawre Baire Aaj", "release_year": 2019, "rental_rate": 3.75, "duration_mins": 115, "genre": "Drama", "director": "Aparna Sen", "total_copies": 4, "available_copies": 4, "rating": 7.2},
        {"name": "Meherjaan", "release_year": 2011, "rental_rate": 3.50, "duration_mins": 108, "genre": "Romance", "director": "Rubaiyat Hossain", "total_copies": 5, "available_copies": 5, "rating": 7.0},
        {"name": "Beta", "release_year": 2012, "rental_rate": 3.25, "duration_mins": 122, "genre": "Drama", "director": "Giasuddin Selim", "total_copies": 4, "available_copies": 4, "rating": 6.9},
        {"name": "Doob", "release_year": 2017, "rental_rate": 3.75, "duration_mins": 125, "genre": "Drama", "director": "Mostofa Sarwar Farooki", "total_copies": 5, "available_copies": 5, "rating": 7.3},
        {"name": "Daruchini Dwip", "release_year": 2007, "rental_rate": 3.50, "duration_mins": 115, "genre": "Drama", "director": "Humayun Ahmed", "total_copies": 4, "available_copies": 4, "rating": 7.1},
        
        {"name": "Mad Max: Fury Road", "release_year": 2015, "rental_rate": 5.00, "duration_mins": 120, "genre": "Action", "director": "George Miller", "total_copies": 9, "available_copies": 9, "rating": 8.1},
        {"name": "Eternal Sunshine of the Spotless Mind", "release_year": 2004, "rental_rate": 4.25, "duration_mins": 108, "genre": "Romance", "director": "Michel Gondry", "total_copies": 6, "available_copies": 6, "rating": 8.3},
        {"name": "Rang De Basanti", "release_year": 2006, "rental_rate": 4.00, "duration_mins": 157, "genre": "Drama", "director": "Rakeysh Omprakash Mehra", "total_copies": 7, "available_copies": 7, "rating": 8.2},
        {"name": "The Handmaiden", "release_year": 2016, "rental_rate": 4.50, "duration_mins": 144, "genre": "Thriller", "director": "Park Chan-wook", "total_copies": 5, "available_copies": 5, "rating": 8.1},
        {"name": "Naree", "release_year": 2014, "rental_rate": 3.50, "duration_mins": 110, "genre": "Drama", "director": "Dipankar Dipon", "total_copies": 4, "available_copies": 4, "rating": 7.0}
    ]

    for data in movies_data:
        movie = Movie(**data)
        session.add(movie)

    session.commit()

    print ("Movies seeded successfully!")

    customers_data = [
        {"first_name": "Anik", "last_name": "Rahman", "email": "anik.rahman@gmail.com", "phone": "+880-1712-345678", "address": "House 14, Road 3, Banani, Dhaka-1213", "created_at": datetime.now()},
        {"first_name": "Shamima", "last_name": "Akter", "email": "shamima.akter@yahoo.com", "phone": "+880-1601-234567", "address": "House 18, Road 5, Banani, Dhaka-1213", "created_at": datetime.now()},
        {"first_name": "Abul", "last_name": "Kalam", "email": "abul.kalam@gmail.com", "phone": "+880-1190-123457", "address": "House 31, Road 7, Banani, Dhaka-1213", "created_at": datetime.now()},
    
        {"first_name": "Faria", "last_name": "Karim", "email": "faria.karim@outlook.com", "phone": "+880-1823-456789", "address": "Flat 7A, Dhanmondi Residential Area, Dhaka-1209", "created_at": datetime.now()},
        {"first_name": "Rafiq", "last_name": "Uddin", "email": "rafiq.uddin@hotmail.com", "phone": "+880-1712-345679", "address": "Flat 3B, Dhanmondi Residential Area, Dhaka-1209", "created_at": datetime.now()},
        {"first_name": "Jesmin", "last_name": "Ara", "email": "jesmin.ara@hotmail.com", "phone": "+880-1601-234568", "address": "Flat 4B, Dhanmondi Residential Area, Dhaka-1209", "created_at": datetime.now()},

        {"first_name": "Sayed", "last_name": "Ahmed", "email": "sayed.ahmed@yahoo.com", "phone": "+880-1934-567890", "address": "Plot 45, Sector 10, Uttara, Dhaka-1230", "created_at": datetime.now()},
        {"first_name": "Sabrina", "last_name": "Yasmin", "email": "sabrina.yasmin@outlook.com", "phone": "+880-1289-012345", "address": "House 36, Sector 11, Uttara, Dhaka-1230", "created_at": datetime.now()},
        {"first_name": "Kamal", "last_name": "Hyder", "email": "kamal.hyder@outlook.com", "phone": "+880-1934-567891", "address": "Plot 67, Sector 12, Uttara, Dhaka-1230", "created_at": datetime.now()},
        {"first_name": "Rashed", "last_name": "Kabir", "email": "rashed.kabir@outlook.com", "phone": "+880-1378-901235", "address": "House 45, Sector 13, Uttara, Dhaka-1230", "created_at": datetime.now()},

        {"first_name": "Tasneem", "last_name": "Islam", "email": "tasneem.islam@gmail.com", "phone": "+880-1645-678901", "address": "House 27, Mirpur DOHS, Dhaka-1216", "created_at": datetime.now()},
        {"first_name": "Romana", "last_name": "Islam", "email": "romana.islam@gmail.com", "phone": "+880-1823-456790", "address": "House 22, Mirpur DOHS, Dhaka-1216", "created_at": datetime.now()},
        {"first_name": "Riaz", "last_name": "Uddin", "email": "riaz.uddin@outlook.com", "phone": "+880-1712-345680", "address": "House 19, Mirpur DOHS, Dhaka-1216", "created_at": datetime.now()},
        {"first_name": "Naimur", "last_name": "Sakib", "email": "droptosakib@gmail.com", "phone": "+880-1522119101", "address": "House 20, Mirpur DOHS, Dhaka-1216", "created_at": datetime.now()},
        
        {"first_name": "Rashid", "last_name": "Khan", "email": "rashid.khan@hotmail.com", "phone": "+880-1556-789012", "address": "Apartment 12C, Mohammadpur Housing, Dhaka-1207", "created_at": datetime.now()},
        {"first_name": "Lubna", "last_name": "Chowdhury", "email": "lubna.chowdhury@yahoo.com", "phone": "+880-1645-678902", "address": "Apartment 8C, Mohammadpur Housing, Dhaka-1207", "created_at": datetime.now()},
        {"first_name": "Nadia", "last_name": "Sultana", "email": "nadia.sultana@gmail.com", "phone": "+880-1467-890123", "address": "House 8, Block B, Lalmatia, Dhaka-1207", "created_at": datetime.now()},
        {"first_name": "Amin", "last_name": "Molla", "email": "amin.molla@gmail.com", "phone": "+880-1556-789013", "address": "House 14, Block C, Lalmatia, Dhaka-1207", "created_at": datetime.now()},

        {"first_name": "Imran", "last_name": "Hossain", "email": "imran.hossain@yahoo.com", "phone": "+880-1378-901234", "address": "Flat 5D, Green Road, Dhaka-1205", "created_at": datetime.now()},
        {"first_name": "Farzana", "last_name": "Begum", "email": "farzana.begum@hotmail.com", "phone": "+880-1467-890124", "address": "Flat 6D, Green Road, Dhaka-1205", "created_at": datetime.now()},
        {"first_name": "Zahid", "last_name": "Mahmud", "email": "zahid.mahmud@gmail.com", "phone": "+880-1190-123456", "address": "Apartment 9A, Kalyanpur, Dhaka-1207", "created_at": datetime.now()},
        {"first_name": "Sharmin", "last_name": "Nahar", "email": "sharmin.nahar@yahoo.com", "phone": "+880-1289-012346", "address": "Apartment 11A, Kalyanpur, Dhaka-1207", "created_at": datetime.now()}
    ]

    for data in customers_data:
        customer = Customer(**data)
        session.add(customer)

    session.commit()

    print ("Customers seeded successfully!")

    session.close()


if __name__ == "__main__":
    seed_database()

    