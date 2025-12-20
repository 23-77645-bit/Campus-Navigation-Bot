"""
Data Access Object for Refill Transaction operations
Handles all database interactions related to refill transactions in water refilling station
"""
from typing import List, Optional
import sqlite3
from datetime import datetime


class RefillTransaction:
    def __init__(self, id=None, customer_id=None, container_id=None, staff_user_id=None, quantity_purchased=0, unit_price=0.0, total_amount=0.0, transaction_date=None, payment_method="cash", transaction_status="completed", notes=""):
        self.id = id
        self.customer_id = customer_id
        self.container_id = container_id
        self.staff_user_id = staff_user_id
        self.quantity_purchased = quantity_purchased
        self.unit_price = unit_price
        self.total_amount = total_amount
        self.transaction_date = transaction_date or datetime.now()
        self.payment_method = payment_method  # 'cash', 'card', 'credit'
        self.transaction_status = transaction_status  # 'completed', 'pending', 'cancelled'
        self.notes = notes


class RefillTransactionDAO:
    def __init__(self, db_path: str = "water_refill_station.db"):
        self.db_path = db_path

    def create_table(self):
        """Create the refill_transactions table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS refill_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                container_id INTEGER NOT NULL,
                staff_user_id INTEGER NOT NULL,
                quantity_purchased INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_amount REAL NOT NULL,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT DEFAULT 'cash',
                transaction_status TEXT DEFAULT 'completed',
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (container_id) REFERENCES water_containers(id),
                FOREIGN KEY (staff_user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_transaction(self, transaction: RefillTransaction) -> bool:
        """Insert a new refill transaction into the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO refill_transactions (customer_id, container_id, staff_user_id, quantity_purchased, unit_price, total_amount, payment_method, transaction_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (transaction.customer_id, transaction.container_id, transaction.staff_user_id, 
                  transaction.quantity_purchased, transaction.unit_price, transaction.total_amount,
                  transaction.payment_method, transaction.transaction_status, transaction.notes))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def get_transaction_by_id(self, transaction_id: int) -> Optional[RefillTransaction]:
        """Retrieve a refill transaction by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, container_id, staff_user_id, quantity_purchased, unit_price, total_amount, 
                         transaction_date, payment_method, transaction_status, notes 
                         FROM refill_transactions WHERE id = ?''', (transaction_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return RefillTransaction(
                id=row[0], 
                customer_id=row[1], 
                container_id=row[2], 
                staff_user_id=row[3], 
                quantity_purchased=row[4], 
                unit_price=row[5], 
                total_amount=row[6], 
                transaction_date=row[7], 
                payment_method=row[8], 
                transaction_status=row[9], 
                notes=row[10]
            )
        return None

    def get_transactions_by_customer(self, customer_id: int) -> List[RefillTransaction]:
        """Retrieve all refill transactions for a specific customer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, container_id, staff_user_id, quantity_purchased, unit_price, total_amount, 
                         transaction_date, payment_method, transaction_status, notes 
                         FROM refill_transactions 
                         WHERE customer_id = ?
                         ORDER BY transaction_date DESC''', (customer_id,))
        rows = cursor.fetchall()
        
        conn.close()
        
        transactions = []
        for row in rows:
            transactions.append(RefillTransaction(
                id=row[0], 
                customer_id=row[1], 
                container_id=row[2], 
                staff_user_id=row[3], 
                quantity_purchased=row[4], 
                unit_price=row[5], 
                total_amount=row[6], 
                transaction_date=row[7], 
                payment_method=row[8], 
                transaction_status=row[9], 
                notes=row[10]
            ))
        
        return transactions

    def get_all_transactions(self) -> List[RefillTransaction]:
        """Retrieve all refill transactions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, container_id, staff_user_id, quantity_purchased, unit_price, total_amount, 
                         transaction_date, payment_method, transaction_status, notes 
                         FROM refill_transactions 
                         ORDER BY transaction_date DESC''')
        rows = cursor.fetchall()
        
        conn.close()
        
        transactions = []
        for row in rows:
            transactions.append(RefillTransaction(
                id=row[0], 
                customer_id=row[1], 
                container_id=row[2], 
                staff_user_id=row[3], 
                quantity_purchased=row[4], 
                unit_price=row[5], 
                total_amount=row[6], 
                transaction_date=row[7], 
                payment_method=row[8], 
                transaction_status=row[9], 
                notes=row[10]
            ))
        
        return transactions

    def update_transaction(self, transaction: RefillTransaction) -> bool:
        """Update an existing refill transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE refill_transactions
            SET customer_id = ?, container_id = ?, staff_user_id = ?, quantity_purchased = ?, 
                unit_price = ?, total_amount = ?, payment_method = ?, transaction_status = ?, notes = ?
            WHERE id = ?
        ''', (transaction.customer_id, transaction.container_id, transaction.staff_user_id, 
              transaction.quantity_purchased, transaction.unit_price, transaction.total_amount,
              transaction.payment_method, transaction.transaction_status, transaction.notes, 
              transaction.id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a refill transaction by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM refill_transactions WHERE id = ?', (transaction_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def get_daily_transactions(self, date: str) -> List[RefillTransaction]:
        """Get all transactions for a specific date (format: YYYY-MM-DD)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, customer_id, container_id, staff_user_id, quantity_purchased, unit_price, total_amount, 
                   transaction_date, payment_method, transaction_status, notes 
            FROM refill_transactions 
            WHERE DATE(transaction_date) = ?
            ORDER BY transaction_date DESC
        ''', (date,))
        rows = cursor.fetchall()
        
        conn.close()
        
        transactions = []
        for row in rows:
            transactions.append(RefillTransaction(
                id=row[0], 
                customer_id=row[1], 
                container_id=row[2], 
                staff_user_id=row[3], 
                quantity_purchased=row[4], 
                unit_price=row[5], 
                total_amount=row[6], 
                transaction_date=row[7], 
                payment_method=row[8], 
                transaction_status=row[9], 
                notes=row[10]
            ))
        
        return transactions

    def get_total_revenue(self) -> float:
        """Get the total revenue from all completed transactions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT SUM(total_amount) FROM refill_transactions WHERE transaction_status = "completed"')
        result = cursor.fetchone()
        
        conn.close()
        
        return result[0] if result[0] else 0.0