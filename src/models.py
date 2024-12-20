from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Index, Enum, Boolean
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Staff(Base):
    __tablename__ = 'staffs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)

    def __repr__(self):
        return f"<Staff {self.username}>"


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    rentals = relationship("Rental", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.first_name} {self.last_name}>"


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    release_year = Column(Integer)
    rental_rate = Column(Float, nullable=False)
    duration_mins = Column(Integer)
    genre = Column(String(50))
    rating = Column(Float, default=0.0)
    director = Column(String(80), nullable=False)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    rentals = relationship("Rental", back_populates="movie")

    # Indexes
    __table_args__ = (Index('idx_movie_name', 'name'),)

    def __repr__(self):
        return f"<Movie {self.name}>"


class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    rental_date = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)
    rental_status = Column(Enum('active', 'returned', 'overdue', name='rental_status_enum'), default='active')
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    customer = relationship("Customer", back_populates="rentals")
    movie = relationship("Movie", back_populates="rentals")
    payments = relationship("Payment", back_populates="rental")
    late_fees = relationship("LateFee", back_populates="rental")

    # Indexes
    __table_args__ = (
        Index('idx_rental_customer', 'customer_id'),
        Index('idx_rental_movie', 'movie_id'),
        Index('idx_rental_status', 'rental_status'),
    )

    def __repr__(self):
        return f"<Rental {self.rental_id}>"


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.now)
    payment_method = Column(Enum('cash', 'credit_card', 'debit_card', name='payment_method_enum'), default='cash')

    # Relationships
    rental = relationship("Rental", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.id}>"
    

class LateFee(Base):
    __tablename__ = 'late_fees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'), nullable=False)
    fee_amount = Column(Float, nullable=False)
    days_late = Column(Integer, nullable=False)
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    rental = relationship("Rental", back_populates="late_fees")

    def __repr__(self):
        return f"<LateFee {self.id}>"
    
