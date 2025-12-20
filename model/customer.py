"""
Customer Model
Represents a customer in the water refilling station system
"""
from datetime import datetime


class Customer:
    def __init__(self, id=None, first_name="", last_name="", email="", phone="", address="", gallons_purchased=0, created_at=None, updated_at=None):
        """
        Initialize a Customer object

        Args:
            id (int, optional): Unique identifier for the customer
            first_name (str): Customer's first name
            last_name (str): Customer's last name
            email (str): Customer's email address
            phone (str): Customer's phone number
            address (str): Customer's address
            gallons_purchased (int): Total gallons purchased by the customer
            created_at (datetime): Creation timestamp
            updated_at (datetime): Last update timestamp
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.gallons_purchased = gallons_purchased
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __str__(self):
        """String representation of the customer"""
        return f"Customer(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')"

    def __repr__(self):
        """Developer-friendly representation of the customer"""
        return self.__str__()

    def to_dict(self):
        """Convert the customer object to a dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'gallons_purchased': self.gallons_purchased,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def get_full_name(self):
        """Get the full name of the customer"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_total_gallons_purchased(self):
        """Get the total gallons purchased by the customer"""
        return self.gallons_purchased