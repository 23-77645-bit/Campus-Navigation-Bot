"""
Water Container Model
Represents a water container in the water refilling station system
"""
from datetime import datetime


class WaterContainer:
    def __init__(self, id=None, container_type="", price_per_unit=0.0, quantity_available=0, size_liters=None, description="", created_at=None, updated_at=None):
        """
        Initialize a WaterContainer object

        Args:
            id (int, optional): Unique identifier for the container
            container_type (str): Type of container ('5gal_jug', 'small_bottle', etc.)
            price_per_unit (float): Price per unit of the container
            quantity_available (int): Quantity available in stock
            size_liters (float, optional): Size in liters
            description (str): Description of the container
            created_at (datetime): Creation timestamp
            updated_at (datetime): Last update timestamp
        """
        self.id = id
        self.container_type = container_type
        self.price_per_unit = price_per_unit
        self.quantity_available = quantity_available
        self.size_liters = size_liters
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __str__(self):
        """String representation of the water container"""
        return f"WaterContainer(id={self.id}, type='{self.container_type}', price={self.price_per_unit})"

    def __repr__(self):
        """Developer-friendly representation of the water container"""
        return self.__str__()

    def to_dict(self):
        """Convert the water container object to a dictionary"""
        return {
            'id': self.id,
            'container_type': self.container_type,
            'price_per_unit': self.price_per_unit,
            'quantity_available': self.quantity_available,
            'size_liters': self.size_liters,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def is_available(self, quantity=1):
        """Check if the specified quantity of containers is available"""
        return self.quantity_available >= quantity

    def get_total_value(self):
        """Get the total value of available containers"""
        return self.quantity_available * self.price_per_unit