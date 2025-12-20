"""
Data Access Object for User operations
Handles all database interactions related to users in water refilling station
"""
from typing import List, Optional
import sqlite3
from model.user import User


class UserDAO:
    def __init__(self, db_path: str = "water_refill_station.db"):
        self.db_path = db_path

    def create_table(self):
        """Create the users table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_user(self, user: User) -> bool:
        """Insert a new user into the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, role)
                VALUES (?, ?, ?, ?)
            ''', (user.username, user.password_hash, user.email, user.role))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Username or email already exists

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, password_hash, email, role FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return User(id=row[0], username=row[1], password_hash=row[2], email=row[3], role=row[4])
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, password_hash, email, role FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return User(id=row[0], username=row[1], password_hash=row[2], email=row[3], role=row[4])
        return None

    def get_all_users(self) -> List[User]:
        """Retrieve all users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, password_hash, email, role FROM users')
        rows = cursor.fetchall()
        
        conn.close()
        
        users = []
        for row in rows:
            users.append(User(id=row[0], username=row[1], password_hash=row[2], email=row[3], role=row[4]))
        
        return users

    def update_user(self, user: User) -> bool:
        """Update an existing user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users
            SET username = ?, password_hash = ?, email = ?, role = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (user.username, user.password_hash, user.email, user.role, user.id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0