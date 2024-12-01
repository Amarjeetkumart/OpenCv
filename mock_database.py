# This file contains functions to interact with a SQLite database to store transactions.
import sqlite3

# Initialize database connection
def init_db():
    conn = sqlite3.connect("transactions.db")  # Creates or connects to the database file
    cursor = conn.cursor()

    # Create a transactions table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name TEXT,
                        final_price REAL,
                        total_price REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    conn.commit()
    conn.close()

# Insert a new transaction into the database
def insert_transaction(products, total_price):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    # Insert each product as a separate row in the transactions table
    for product in products:
        cursor.execute('''INSERT INTO transactions (product_name, final_price, total_price) 
                          VALUES (?, ?, ?)''', (product["name"], product["final_price"], total_price))
    conn.commit()
    conn.close()

# Fetch all transactions (for debugging or display purposes)
def fetch_transactions():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    # Fetch all rows from the transactions table
    cursor.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()
    conn.close()
    return rows
# Path: qr_code_generator.py