"""
Data Access Object for Water Container operations
Handles all database interactions related to water containers in water refilling station
"""
from typing import List, Optional
import sqlite3
from model.water_container import WaterContainer


class WaterContainerDAO:
    def __init__(self, db_path: str = "water_refill_station.db"):
        self.db_path = db_path

    def create_table(self):
        """Create the water_containers table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()

    def create_water_container(self, container: WaterContainer) -> bool:
        """Insert a new water container into the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO water_containers (container_type, price_per_unit, quantity_available, size_liters, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (container.container_type, container.price_per_unit, container.quantity_available, 
                  container.size_liters, container.description))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def get_container_by_id(self, container_id: int) -> Optional[WaterContainer]:
        """Retrieve a water container by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, container_type, price_per_unit, quantity_available, size_liters, description, created_at, updated_at
                         FROM water_containers WHERE id = ?''', (container_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return WaterContainer(
                id=row[0], 
                container_type=row[1], 
                price_per_unit=row[2], 
                quantity_available=row[3],
                size_liters=row[4],
                description=row[5],
                created_at=row[6],
                updated_at=row[7]
            )
        return None

    def get_container_by_type(self, container_type: str) -> Optional[WaterContainer]:
        """Retrieve a water container by type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, container_type, price_per_unit, quantity_available, size_liters, description, created_at, updated_at
                         FROM water_containers WHERE container_type = ?''', (container_type,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return WaterContainer(
                id=row[0], 
                container_type=row[1], 
                price_per_unit=row[2], 
                quantity_available=row[3],
                size_liters=row[4],
                description=row[5],
                created_at=row[6],
                updated_at=row[7]
            )
        return None

    def get_all_containers(self) -> List[WaterContainer]:
        """Retrieve all water containers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, container_type, price_per_unit, quantity_available, size_liters, description, created_at, updated_at
                         FROM water_containers ORDER BY container_type''')
        rows = cursor.fetchall()
        
        conn.close()
        
        containers = []
        for row in rows:
            containers.append(WaterContainer(
                id=row[0], 
                container_type=row[1], 
                price_per_unit=row[2], 
                quantity_available=row[3],
                size_liters=row[4],
                description=row[5],
                created_at=row[6],
                updated_at=row[7]
            ))
        
        return containers

    def update_container(self, container: WaterContainer) -> bool:
        """Update an existing water container"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE water_containers
            SET container_type = ?, price_per_unit = ?, quantity_available = ?, 
                size_liters = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (container.container_type, container.price_per_unit, container.quantity_available, 
              container.size_liters, container.description, container.id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def delete_container(self, container_id: int) -> bool:
        """Delete a water container by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM water_containers WHERE id = ?', (container_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def update_quantity(self, container_id: int, new_quantity: int) -> bool:
        """Update the quantity available for a specific container"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE water_containers
            SET quantity_available = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_quantity, container_id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def decrease_quantity(self, container_id: int, quantity_to_decrease: int) -> bool:
        """Decrease the quantity available for a specific container"""
        container = self.get_container_by_id(container_id)
        if not container:
            return False
        
        new_quantity = max(0, container.quantity_available - quantity_to_decrease)
        return self.update_quantity(container_id, new_quantity)

    def increase_quantity(self, container_id: int, quantity_to_increase: int) -> bool:
        """Increase the quantity available for a specific container"""
        container = self.get_container_by_id(container_id)
        if not container:
            return False
        
        new_quantity = container.quantity_available + quantity_to_increase
        return self.update_quantity(container_id, new_quantity)