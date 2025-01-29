import sqlite3

# Database connection function
def get_db_connection():
    connection = sqlite3.connect('books.db')  # SQLite database file
    connection.row_factory = sqlite3.Row       # Enables dictionary-like access
    return connection

# Create a sample table and seed data
def initialize_database():
    connection = get_db_connection()
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        connection.execute("""
            INSERT INTO users (name, age)
            VALUES ('Alice', 30), ('Bob', 25)
            ON CONFLICT DO NOTHING
        """)
    connection.close()

# Initialize the database when the script runs
initialize_database()