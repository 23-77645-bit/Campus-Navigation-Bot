"""
Database initialization module
Creates SQLite database file and initializes schema for Water Refilling Station
"""
import sqlite3
import os


def initialize_database(db_path="water_refill_station.db"):
    """
    Initialize the database with required tables for water refilling station
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,  -- 'admin' or 'staff'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            gallons_purchased INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create water containers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS water_containers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            container_type TEXT NOT NULL, -- '5gal_jug', 'small_bottle', etc.
            price_per_unit REAL NOT NULL,
            quantity_available INTEGER DEFAULT 0,
            size_liters REAL, -- Size in liters
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create refill transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS refill_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            container_id INTEGER NOT NULL,
            staff_user_id INTEGER NOT NULL,
            quantity_purchased INTEGER NOT NULL, -- Number of units purchased
            unit_price REAL NOT NULL, -- Price per unit at time of transaction
            total_amount REAL NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            payment_method TEXT DEFAULT 'cash', -- 'cash', 'card', 'credit'
            transaction_status TEXT DEFAULT 'completed', -- 'completed', 'pending', 'cancelled'
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (container_id) REFERENCES water_containers(id),
            FOREIGN KEY (staff_user_id) REFERENCES users(id)
        )
    ''')
    
    # Create customer deposits table for deposit tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_deposits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            container_type TEXT NOT NULL, -- Type of container deposited
            quantity INTEGER NOT NULL, -- Number of containers
            deposit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active', -- 'active', 'returned', 'lost'
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')
    
    # Create audit log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            table_affected TEXT,
            record_id INTEGER,
            old_values TEXT,
            new_values TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database '{db_path}' initialized successfully!")


if __name__ == "__main__":
    initialize_database()