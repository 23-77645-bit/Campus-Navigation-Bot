"""
Admin Activity Logger Service
Logs administrative actions for audit purposes
"""
import sqlite3
from datetime import datetime
from model.user import User


class AdminActivityLogger:
    def __init__(self, db_path: str = "library_system.db"):
        self.db_path = db_path
        self._ensure_audit_table_exists()

    def _ensure_audit_table_exists(self):
        """Ensure the audit logs table exists in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()

    def log_action(self, user: User, action: str, table_affected: str = None, 
                   record_id: int = None, old_values: dict = None, new_values: dict = None):
        """
        Log an administrative action
        
        Args:
            user (User): The user performing the action
            action (str): Description of the action taken
            table_affected (str, optional): Name of the table affected
            record_id (int, optional): ID of the record affected
            old_values (dict, optional): Dictionary of old values before change
            new_values (dict, optional): Dictionary of new values after change
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert dictionaries to JSON-like strings
        old_values_str = str(old_values) if old_values else None
        new_values_str = str(new_values) if new_values else None
        
        cursor.execute('''
            INSERT INTO audit_logs (user_id, action, table_affected, record_id, old_values, new_values)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user.id, action, table_affected, record_id, old_values_str, new_values_str))
        
        conn.commit()
        conn.close()

    def log_user_creation(self, admin_user: User, created_user: User):
        """Log when an admin creates a new user"""
        self.log_action(
            user=admin_user,
            action="USER_CREATED",
            table_affected="users",
            record_id=created_user.id,
            new_values=created_user.to_dict()
        )

    def log_user_update(self, admin_user: User, updated_user: User, old_values: dict):
        """Log when an admin updates a user"""
        self.log_action(
            user=admin_user,
            action="USER_UPDATED",
            table_affected="users",
            record_id=updated_user.id,
            old_values=old_values,
            new_values=updated_user.to_dict()
        )

    def log_user_deletion(self, admin_user: User, deleted_user_id: int):
        """Log when an admin deletes a user"""
        self.log_action(
            user=admin_user,
            action="USER_DELETED",
            table_affected="users",
            record_id=deleted_user_id
        )

    def log_product_addition(self, admin_user: User, product):
        """Log when an admin adds a new product"""
        self.log_action(
            user=admin_user,
            action="PRODUCT_ADDED",
            table_affected="products",
            record_id=getattr(product, 'id', None),
            new_values={
                'name': getattr(product, 'name', ''),
                'category': getattr(product, 'category', ''),
                'price': getattr(product, 'price', 0),
                'quantity_available': getattr(product, 'quantity_available', 0)
            }
        )

    def get_audit_logs(self, limit: int = 100) -> list:
        """
        Retrieve audit logs (most recent first)
        
        Args:
            limit (int): Maximum number of logs to retrieve
            
        Returns:
            list: List of audit log entries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT al.timestamp, u.username, al.action, al.table_affected, 
                   al.record_id, al.old_values, al.new_values
            FROM audit_logs al
            JOIN users u ON al.user_id = u.id
            ORDER BY al.timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                'timestamp': row[0],
                'username': row[1],
                'action': row[2],
                'table_affected': row[3],
                'record_id': row[4],
                'old_values': row[5],
                'new_values': row[6]
            })
        
        return logs

    def get_user_audit_logs(self, user_id: int) -> list:
        """
        Retrieve audit logs for a specific user
        
        Args:
            user_id (int): ID of the user to get logs for
            
        Returns:
            list: List of audit log entries for the user
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT al.timestamp, u.username, al.action, al.table_affected, 
                   al.record_id, al.old_values, al.new_values
            FROM audit_logs al
            JOIN users u ON al.user_id = u.id
            WHERE al.user_id = ?
            ORDER BY al.timestamp DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                'timestamp': row[0],
                'username': row[1],
                'action': row[2],
                'table_affected': row[3],
                'record_id': row[4],
                'old_values': row[5],
                'new_values': row[6]
            })
        
        return logs