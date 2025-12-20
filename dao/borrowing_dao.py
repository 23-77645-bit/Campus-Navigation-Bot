"""
Data Access Object for Customer Deposit operations
Handles all database interactions related to customer deposits in water refilling station
"""
from typing import List, Optional
import sqlite3
from datetime import datetime


class CustomerDeposit:
    def __init__(self, id=None, customer_id=None, container_type="", quantity=0, 
                 deposit_date=None, status='active', notes=''):
        self.id = id
        self.customer_id = customer_id
        self.container_type = container_type  # Type of container deposited
        self.quantity = quantity  # Number of containers
        self.deposit_date = deposit_date or datetime.now()
        self.status = status  # 'active', 'returned', 'lost'
        self.notes = notes


class CustomerDepositDAO:
    def __init__(self, db_path: str = "water_refill_station.db"):
        self.db_path = db_path

    def create_table(self):
        """Create the customer_deposits table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_deposits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                container_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                deposit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_deposit(self, deposit: CustomerDeposit) -> bool:
        """Insert a new customer deposit record into the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO customer_deposits (customer_id, container_type, quantity, status, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (deposit.customer_id, deposit.container_type, deposit.quantity, 
                  deposit.status, deposit.notes))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def get_deposit_by_id(self, deposit_id: int) -> Optional[CustomerDeposit]:
        """Retrieve a customer deposit record by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, container_type, quantity, 
                         deposit_date, status, notes 
                         FROM customer_deposits WHERE id = ?''', (deposit_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return CustomerDeposit(
                id=row[0], 
                customer_id=row[1], 
                container_type=row[2], 
                quantity=row[3], 
                deposit_date=row[4], 
                status=row[5], 
                notes=row[6]
            )
        return None

    def get_all_deposits(self) -> List[CustomerDeposit]:
        """Retrieve all customer deposit records"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, container_type, quantity, 
                         deposit_date, status, notes 
                         FROM customer_deposits
                         ORDER BY deposit_date DESC''')
        rows = cursor.fetchall()
        
        conn.close()
        
        deposits = []
        for row in rows:
            deposits.append(CustomerDeposit(
                id=row[0], 
                customer_id=row[1], 
                container_type=row[2], 
                quantity=row[3], 
                deposit_date=row[4], 
                status=row[5], 
                notes=row[6]
            ))
        
        return deposits

    def get_deposits_by_customer(self, customer_id: int) -> List[CustomerDeposit]:
        """Retrieve all deposits for a specific customer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, container_type, quantity, 
                         deposit_date, status, notes 
                         FROM customer_deposits WHERE customer_id = ?
                         ORDER BY deposit_date DESC''', (customer_id,))
        rows = cursor.fetchall()
        
        conn.close()
        
        deposits = []
        for row in rows:
            deposits.append(CustomerDeposit(
                id=row[0], 
                customer_id=row[1], 
                container_type=row[2], 
                quantity=row[3], 
                deposit_date=row[4], 
                status=row[5], 
                notes=row[6]
            ))
        
        return deposits

    def get_active_deposits(self) -> List[CustomerDeposit]:
        """Retrieve all active deposits"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, container_type, quantity, 
                         deposit_date, status, notes 
                         FROM customer_deposits WHERE status = 'active' 
                         ORDER BY deposit_date DESC''')
        rows = cursor.fetchall()
        
        conn.close()
        
        deposits = []
        for row in rows:
            deposits.append(CustomerDeposit(
                id=row[0], 
                customer_id=row[1], 
                container_type=row[2], 
                quantity=row[3], 
                deposit_date=row[4], 
                status=row[5], 
                notes=row[6]
            ))
        
        return deposits

    def update_deposit(self, deposit: CustomerDeposit) -> bool:
        """Update an existing customer deposit record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE customer_deposits
            SET customer_id = ?, container_type = ?, quantity = ?, 
                status = ?, notes = ?
            WHERE id = ?
        ''', (deposit.customer_id, deposit.container_type, deposit.quantity, 
              deposit.status, deposit.notes, deposit.id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def delete_deposit(self, deposit_id: int) -> bool:
        """Delete a customer deposit record by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM customer_deposits WHERE id = ?', (deposit_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def mark_deposit_returned(self, deposit_id: int) -> bool:
        """Mark a deposit as returned"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE customer_deposits
            SET status = 'returned'
            WHERE id = ?
        ''', (deposit_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def mark_deposit_lost(self, deposit_id: int) -> bool:
        """Mark a deposit as lost"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE customer_deposits
            SET status = 'lost'
            WHERE id = ?
        ''', (deposit_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0