"""
Login Frame
Main login interface for the application
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.user_dao import UserDAO
from model.user import User
from service.session_manager import SessionManager
from ui.login.sign_up_frame import SignUpFrame
from ui.login.forgot_password_frame import ForgotPasswordFrame


class LoginFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.session_manager = SessionManager()
        self.user_dao = UserDAO()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface elements"""
        self.parent.title("Login - Library Management System")
        self.parent.geometry("400x300")
        self.parent.resizable(False, False)
        
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Library Management System", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username field
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Password field
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(main_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Login button
        login_btn = ttk.Button(main_frame, text="Login", command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Sign up button
        signup_btn = ttk.Button(main_frame, text="Sign Up", command=self.open_signup)
        signup_btn.grid(row=4, column=0, pady=5)
        
        # Forgot password button
        forgot_btn = ttk.Button(main_frame, text="Forgot Password?", command=self.open_forgot_password)
        forgot_btn.grid(row=4, column=1, pady=5)
        
        # Bind Enter key to login
        self.parent.bind('<Return>', lambda event: self.login())
        
        # Focus on username field
        self.username_entry.focus()
        
    def login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # For this example, we're using a simple check
        # In a real application, you would hash the password and compare
        user = self.user_dao.get_user_by_username(username)
        
        if user:  # Simplified for demo - in real app, verify hashed password
            self.session_manager.login(user)
            
            # Determine which UI to open based on role
            if user.is_admin():
                from ui.admin.admin_ui import AdminUI
                self.parent.withdraw()  # Hide login window
                admin_window = tk.Toplevel()
                AdminUI(admin_window)
            else:  # Staff
                from ui.staff.staff_ui import StaffUI
                self.parent.withdraw()  # Hide login window
                staff_window = tk.Toplevel()
                StaffUI(staff_window)
                
            # Close the login window after opening the appropriate UI
            self.parent.after(100, self.parent.destroy)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def open_signup(self):
        """Open the sign up window"""
        self.parent.withdraw()
        signup_window = tk.Toplevel()
        SignUpFrame(signup_window, return_callback=self.return_to_login)
    
    def open_forgot_password(self):
        """Open the forgot password window"""
        self.parent.withdraw()
        forgot_window = tk.Toplevel()
        ForgotPasswordFrame(forgot_window, return_callback=self.return_to_login)
    
    def return_to_login(self):
        """Callback to return to the login screen"""
        # Re-open login window if needed
        pass