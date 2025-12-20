"""
Data Access Object for Borrowing operations
Handles all database interactions related to borrowings
"""
from typing import List, Optional
import sqlite3
from datetime import datetime


class Borrowing:
    def __init__(self, id=None, customer_id=None, product_id=None, borrowed_by_user_id=None, 
                 borrowed_date=None, due_date=None, returned_date=None, status='borrowed', notes=''):
        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.borrowed_by_user_id = borrowed_by_user_id
        self.borrowed_date = borrowed_date or datetime.now()
        self.due_date = due_date
        self.returned_date = returned_date
        self.status = status  # 'borrowed', 'returned', 'overdue'
        self.notes = notes


class BorrowingDAO:
    def __init__(self, db_path: str = "library_system.db"):
        self.db_path = db_path

    def create_table(self):
        """Create the borrowings table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                borrowed_by_user_id INTEGER NOT NULL,
                borrowed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                returned_date TIMESTAMP,
                status TEXT DEFAULT 'borrowed',
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (borrowed_by_user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_borrowing(self, borrowing: Borrowing) -> bool:
        """Insert a new borrowing record into the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO borrowings (customer_id, product_id, borrowed_by_user_id, 
                                       borrowed_date, due_date, returned_date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (borrowing.customer_id, borrowing.product_id, borrowing.borrowed_by_user_id,
                  borrowing.borrowed_date, borrowing.due_date, borrowing.returned_date, 
                  borrowing.status, borrowing.notes))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def get_borrowing_by_id(self, borrowing_id: int) -> Optional[Borrowing]:
        """Retrieve a borrowing record by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, product_id, borrowed_by_user_id, 
                         borrowed_date, due_date, returned_date, status, notes 
                         FROM borrowings WHERE id = ?''', (borrowing_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Borrowing(id=row[0], customer_id=row[1], product_id=row[2], 
                            borrowed_by_user_id=row[3], borrowed_date=row[4], 
                            due_date=row[5], returned_date=row[6], status=row[7], notes=row[8])
        return None

    def get_all_borrowings(self) -> List[Borrowing]:
        """Retrieve all borrowing records"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, product_id, borrowed_by_user_id, 
                         borrowed_date, due_date, returned_date, status, notes 
                         FROM borrowings''')
        rows = cursor.fetchall()
        
        conn.close()
        
        borrowings = []
        for row in rows:
            borrowings.append(Borrowing(id=row[0], customer_id=row[1], product_id=row[2], 
                                       borrowed_by_user_id=row[3], borrowed_date=row[4], 
                                       due_date=row[5], returned_date=row[6], status=row[7], notes=row[8]))
        
        return borrowings

    def get_borrowings_by_customer(self, customer_id: int) -> List[Borrowing]:
        """Retrieve all borrowings for a specific customer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, product_id, borrowed_by_user_id, 
                         borrowed_date, due_date, returned_date, status, notes 
                         FROM borrowings WHERE customer_id = ?''', (customer_id,))
        rows = cursor.fetchall()
        
        conn.close()
        
        borrowings = []
        for row in rows:
            borrowings.append(Borrowing(id=row[0], customer_id=row[1], product_id=row[2], 
                                       borrowed_by_user_id=row[3], borrowed_date=row[4], 
                                       due_date=row[5], returned_date=row[6], status=row[7], notes=row[8]))
        
        return borrowings

    def get_active_borrowings(self) -> List[Borrowing]:
        """Retrieve all active borrowings (not returned)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, customer_id, product_id, borrowed_by_user_id, 
                         borrowed_date, due_date, returned_date, status, notes 
                         FROM borrowings WHERE status = 'borrowed' ''')
        rows = cursor.fetchall()
        
        conn.close()
        
        borrowings = []
        for row in rows:
            borrowings.append(Borrowing(id=row[0], customer_id=row[1], product_id=row[2], 
                                       borrowed_by_user_id=row[3], borrowed_date=row[4], 
                                       due_date=row[5], returned_date=row[6], status=row[7], notes=row[8]))
        
        return borrowings

    def update_borrowing(self, borrowing: Borrowing) -> bool:
        """Update an existing borrowing record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE borrowings
            SET customer_id = ?, product_id = ?, borrowed_by_user_id = ?, 
                borrowed_date = ?, due_date = ?, returned_date = ?, status = ?, notes = ?
            WHERE id = ?
        ''', (borrowing.customer_id, borrowing.product_id, borrowing.borrowed_by_user_id,
              borrowing.borrowed_date, borrowing.due_date, borrowing.returned_date, 
              borrowing.status, borrowing.notes, borrowing.id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def delete_borrowing(self, borrowing_id: int) -> bool:
        """Delete a borrowing record by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM borrowings WHERE id = ?', (borrowing_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0