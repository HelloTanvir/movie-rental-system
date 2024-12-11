# Rent a Movie

A Python-based movie rental management system that helps you manage your movie inventory and rental operations.

## Prerequisites

Before running this project, make sure you have the following installed on your system:

- Python 3.9 or higher
- Docker Desktop ([Download here](https://www.docker.com/products/docker-desktop/))
- Git (for cloning the repository)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/HelloTanvir/movie-rental-system.git
cd movie-rental-system
```

### 2. Start the Database

The project uses PostgreSQL running in a Docker container. Start it using:

```bash
docker-compose up -d
```

### 3. Set Up Python Environment

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
# If you are using default terminal
.\venv\Scripts\activate
# If you are using git bash terminal
source ./venv/Scripts/activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory using `.env.example` as a template:

```bash
cp .env.example .env
```

Open `.env` and update the values according to your setup. Example:

```plaintext
POSTGRES_HOST = db
POSTGRES_PORT = 5432
POSTGRES_USER = tanvir
POSTGRES_PASSWORD = tanvir
POSTGRES_DB = movie-rental-db

# Other configuration variables...
```

### 6. Run the Application

Navigate to the src directory and run the main application:

```bash
python ./src/main.py
```

## Database Administration

To access the PostgreSQL database through a web interface:

1. Open your web browser and go to `http://localhost:8080`
2. Log in using the credentials you set in your `.env` file:
   - System: PostgreSQL
   - Server: db
   - Username: (DB_USER from .env)
   - Password: (DB_PASSWORD from .env)
   - Database: (DB_NAME from .env)

## Troubleshooting

If you encounter any issues:

1. Ensure Docker Desktop is running
2. Check if the database container is up:
   ```bash
   docker ps
   ```
3. Verify your `.env` file configurations match your Docker setup
4. Make sure all required ports (8080, 5432) are not being used by other applications