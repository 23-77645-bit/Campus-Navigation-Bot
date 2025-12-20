"""
Session Manager Service
Manages user sessions and authentication state
"""
from model.user import User


class SessionManager:
    _instance = None
    _current_user = None

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def login(self, user: User):
        """Log in a user and store their session"""
        self._current_user = user

    def logout(self):
        """Log out the current user"""
        self._current_user = None

    def get_current_user(self) -> User:
        """Get the currently logged-in user"""
        return self._current_user

    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in"""
        return self._current_user is not None

    def has_role(self, role: str) -> bool:
        """Check if the current user has a specific role"""
        if self._current_user:
            return self._current_user.role.lower() == role.lower()
        return False

    def is_admin(self) -> bool:
        """Check if the current user is an admin"""
        return self.has_role('admin')

    def is_staff(self) -> bool:
        """Check if the current user is a staff member"""
        return self.has_role('staff')