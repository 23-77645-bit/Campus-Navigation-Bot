"""
Data Access Object for Customer operations
Handles all database interactions related to customers in water refilling station
"""
from typing import List, Optional
import sqlite3
from model.customer import Customer


class CustomerDAO:
    def __init__(self, db_path: str = "water_refill_station.db"):
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
                gallons_purchased INTEGER DEFAULT 0,
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
                INSERT INTO customers (first_name, last_name, email, phone, address, gallons_purchased)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer.first_name, customer.last_name, customer.email, 
                  customer.phone, customer.address, customer.gallons_purchased))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Email already exists

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, first_name, last_name, email, phone, address, gallons_purchased, created_at, updated_at
                         FROM customers WHERE id = ?''', (customer_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Customer(
                id=row[0], 
                first_name=row[1], 
                last_name=row[2], 
                email=row[3], 
                phone=row[4], 
                address=row[5],
                gallons_purchased=row[6],
                created_at=row[7],
                updated_at=row[8]
            )
        return None

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Retrieve a customer by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, first_name, last_name, email, phone, address, gallons_purchased, created_at, updated_at
                         FROM customers WHERE email = ?''', (email,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Customer(
                id=row[0], 
                first_name=row[1], 
                last_name=row[2], 
                email=row[3], 
                phone=row[4], 
                address=row[5],
                gallons_purchased=row[6],
                created_at=row[7],
                updated_at=row[8]
            )
        return None

    def get_all_customers(self) -> List[Customer]:
        """Retrieve all customers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, first_name, last_name, email, phone, address, gallons_purchased, created_at, updated_at
                         FROM customers ORDER BY last_name, first_name''')
        rows = cursor.fetchall()
        
        conn.close()
        
        customers = []
        for row in rows:
            customers.append(Customer(
                id=row[0], 
                first_name=row[1], 
                last_name=row[2], 
                email=row[3], 
                phone=row[4], 
                address=row[5],
                gallons_purchased=row[6],
                created_at=row[7],
                updated_at=row[8]
            ))
        
        return customers

    def update_customer(self, customer: Customer) -> bool:
        """Update an existing customer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE customers
            SET first_name = ?, last_name = ?, email = ?, phone = ?, 
                address = ?, gallons_purchased = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (customer.first_name, customer.last_name, customer.email, 
              customer.phone, customer.address, customer.gallons_purchased, customer.id))
        
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
        """Search customers by first name, last name, or email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        search_pattern = f"%{search_term}%"
        cursor.execute('''
            SELECT id, first_name, last_name, email, phone, address, gallons_purchased, created_at, updated_at 
            FROM customers 
            WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
            ORDER BY last_name, first_name
        ''', (search_pattern, search_pattern, search_pattern))
        rows = cursor.fetchall()
        
        conn.close()
        
        customers = []
        for row in rows:
            customers.append(Customer(
                id=row[0], 
                first_name=row[1], 
                last_name=row[2], 
                email=row[3], 
                phone=row[4], 
                address=row[5],
                gallons_purchased=row[6],
                created_at=row[7],
                updated_at=row[8]
            ))
        
        return customers