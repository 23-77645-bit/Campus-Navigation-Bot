"""
Sign Up Frame
Registration interface for new users
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.user_dao import UserDAO
from model.user import User


class SignUpFrame(tk.Frame):
    def __init__(self, parent, return_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.return_callback = return_callback
        self.user_dao = UserDAO()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface elements"""
        self.parent.title("Sign Up - Library Management System")
        self.parent.geometry("400x350")
        self.parent.resizable(False, False)
        
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Create New Account", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username field
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Email field
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(main_frame, width=30)
        self.email_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Password field
        ttk.Label(main_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(main_frame, width=30, show="*")
        self.password_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Confirm Password field
        ttk.Label(main_frame, text="Confirm Password:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.confirm_password_entry = ttk.Entry(main_frame, width=30, show="*")
        self.confirm_password_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # Role selection
        ttk.Label(main_frame, text="Role:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar(value="staff")
        role_combo = ttk.Combobox(main_frame, textvariable=self.role_var, 
                                  values=["admin", "staff"], state="readonly", width=27)
        role_combo.grid(row=5, column=1, pady=5, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Sign Up button
        signup_btn = ttk.Button(button_frame, text="Sign Up", command=self.signup)
        signup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side=tk.LEFT)
        
        # Bind Enter key to signup
        self.parent.bind('<Return>', lambda event: self.signup())
        
        # Focus on username field
        self.username_entry.focus()
        
    def signup(self):
        """Handle user registration"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        role = self.role_var.get()
        
        # Validation
        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
            
        # Check if email is valid (basic check)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        # Create user object (in real app, hash the password)
        # For demo purposes, we'll store the plain password
        user = User(username=username, password_hash=password, email=email, role=role)
        
        # Attempt to create user
        success = self.user_dao.create_user(user)
        
        if success:
            messagebox.showinfo("Success", "Account created successfully!")
            self.cancel()  # Return to login
        else:
            messagebox.showerror("Error", "Username or email already exists")
    
    def cancel(self):
        """Cancel registration and return to login"""
        self.parent.destroy()
        if self.return_callback:
            self.return_callback()