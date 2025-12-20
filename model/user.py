"""
User Model
Represents a user in the system with attributes like username, email, role, etc.
"""


class User:
    def __init__(self, id=None, username="", password_hash="", email="", role=""):
        """
        Initialize a User object
        
        Args:
            id (int, optional): Unique identifier for the user
            username (str): The user's username
            password_hash (str): Hashed password
            email (str): The user's email address
            role (str): The user's role ('admin' or 'staff')
        """
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.role = role  # 'admin' or 'staff'

    def __str__(self):
        """String representation of the user"""
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}')"

    def __repr__(self):
        """Developer-friendly representation of the user"""
        return self.__str__()

    def to_dict(self):
        """Convert the user object to a dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }

    def is_admin(self):
        """Check if the user has admin privileges"""
        return self.role.lower() == 'admin'

    def is_staff(self):
        """Check if the user has staff privileges"""
        return self.role.lower() == 'staff'