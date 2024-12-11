import random
from models import Customer, Movie


def seed_database(session, num_customers: int = 50, num_movies: int = 30):
    # Seed Customers
    customers = []
    for i in range(num_customers):
        customer = Customer(
            first_name=f'Customer-{i+1}',
            last_name='',
            email=f'test-{i+1}@gmail.com',
            phone=f'01813474764{i}',
            address=f'House-{i+1}, Road-{i+1}, Block-{i+1}, Dhaka',
        )
        customers.append(customer)
    
    # Seed Movies
    movies = []
    genres = [
        'Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 
        'Romance', 'Thriller', 'Documentary', 'Fantasy', 'Adventure'
    ]
    for _ in range(num_movies):
        total_copies = random.randint(10, 100)
        movie = Movie(
            name=f'Movie-{_+1}',
            release_year=random.randint(1990, 2021),
            rental_rate=round(random.uniform(1.99, 9.99), 2),
            duration_mins=random.randint(60, 240),
            genre=random.choice(genres),
            rating=round(random.uniform(0.0, 5.0), 1),
            director=f'Director-{_+1}',
            total_copies=total_copies,
            available_copies=random.randint(0, total_copies),
        )
        movies.append(movie)
    
    # Add to session and commit
    session.add_all(customers)
    session.add_all(movies)
    session.commit()

    print(f"Seeded {len(customers)} customers and {len(movies)} movies.")