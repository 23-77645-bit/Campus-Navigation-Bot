"""
Data Access Object for Customer operations
Handles all database interactions related to customers
"""
from typing import List, Optional
import sqlite3


class Customer:
    def __init__(self, id=None, first_name="", last_name="", email="", phone="", address=""):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address


class CustomerDAO:
    def __init__(self, db_path: str = "library_system.db"):
        self.db_path = db_path

    def create_table(self):
        """Create the customers table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_customer(self, customer: Customer) -> bool:
        """Insert a new customer into the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO customers (first_name, last_name, email, phone, address)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer.first_name, customer.last_name, customer.email, 
                  customer.phone, customer.address))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Email already exists

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, first_name, last_name, email, phone, address 
                         FROM customers WHERE id = ?''', (customer_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Customer(id=row[0], first_name=row[1], last_name=row[2], 
                           email=row[3], phone=row[4], address=row[5])
        return None

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Retrieve a customer by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, first_name, last_name, email, phone, address 
                         FROM customers WHERE email = ?''', (email,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Customer(id=row[0], first_name=row[1], last_name=row[2], 
                           email=row[3], phone=row[4], address=row[5])
        return None

    def get_all_customers(self) -> List[Customer]:
        """Retrieve all customers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, first_name, last_name, email, phone, address 
                         FROM customers''')
        rows = cursor.fetchall()
        
        conn.close()
        
        customers = []
        for row in rows:
            customers.append(Customer(id=row[0], first_name=row[1], last_name=row[2], 
                                     email=row[3], phone=row[4], address=row[5]))
        
        return customers

    def update_customer(self, customer: Customer) -> bool:
        """Update an existing customer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE customers
            SET first_name = ?, last_name = ?, email = ?, phone = ?, 
                address = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (customer.first_name, customer.last_name, customer.email, 
              customer.phone, customer.address, customer.id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def search_customers(self, search_term: str) -> List[Customer]:
        """Search customers by name or email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, first_name, last_name, email, phone, address 
                         FROM customers 
                         WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?''', 
                      (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()
        
        conn.close()
        
        customers = []
        for row in rows:
            customers.append(Customer(id=row[0], first_name=row[1], last_name=row[2], 
                                     email=row[3], phone=row[4], address=row[5]))
        
        return customers