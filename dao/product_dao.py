"""
Data Access Object for Product operations
Handles all database interactions related to products
"""
from typing import List, Optional
import sqlite3


class Product:
    def __init__(self, id=None, name="", description="", category="", price=0.0, quantity_available=0, qr_code=None):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.quantity_available = quantity_available
        self.qr_code = qr_code


class ProductDAO:
    def __init__(self, db_path: str = "library_system.db"):
        self.db_path = db_path

    def create_table(self):
        """Create the products table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                price REAL,
                quantity_available INTEGER DEFAULT 0,
                qr_code TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_product(self, product: Product) -> bool:
        """Insert a new product into the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO products (name, description, category, price, quantity_available, qr_code)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (product.name, product.description, product.category, 
                  product.price, product.quantity_available, product.qr_code))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a product by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, name, description, category, price, 
                         quantity_available, qr_code FROM products WHERE id = ?''', (product_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Product(id=row[0], name=row[1], description=row[2], 
                          category=row[3], price=row[4], quantity_available=row[5], qr_code=row[6])
        return None

    def get_all_products(self) -> List[Product]:
        """Retrieve all products"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, name, description, category, price, 
                         quantity_available, qr_code FROM products''')
        rows = cursor.fetchall()
        
        conn.close()
        
        products = []
        for row in rows:
            products.append(Product(id=row[0], name=row[1], description=row[2], 
                                   category=row[3], price=row[4], quantity_available=row[5], qr_code=row[6]))
        
        return products

    def update_product(self, product: Product) -> bool:
        """Update an existing product"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products
            SET name = ?, description = ?, category = ?, price = ?, 
                quantity_available = ?, qr_code = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (product.name, product.description, product.category, 
              product.price, product.quantity_available, product.qr_code, product.id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def delete_product(self, product_id: int) -> bool:
        """Delete a product by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def search_products(self, search_term: str) -> List[Product]:
        """Search products by name or description"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, name, description, category, price, 
                         quantity_available, qr_code FROM products 
                         WHERE name LIKE ? OR description LIKE ?''', 
                      (f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()
        
        conn.close()
        
        products = []
        for row in rows:
            products.append(Product(id=row[0], name=row[1], description=row[2], 
                                   category=row[3], price=row[4], quantity_available=row[5], qr_code=row[6]))
        
        return products