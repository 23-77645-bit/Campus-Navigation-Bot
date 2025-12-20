"""
Forgot Password Frame
Interface for password recovery
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.user_dao import UserDAO


class ForgotPasswordFrame(tk.Frame):
    def __init__(self, parent, return_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.return_callback = return_callback
        self.user_dao = UserDAO()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface elements"""
        self.parent.title("Forgot Password - Library Management System")
        self.parent.geometry("400x200")
        self.parent.resizable(False, False)
        
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Password Recovery", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, text="Enter your email address to reset your password:")
        instructions.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Email field
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.email_entry = ttk.Entry(main_frame, width=30)
        self.email_entry.grid(row=2, column=1, pady=10, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Submit button
        submit_btn = ttk.Button(button_frame, text="Submit", command=self.submit)
        submit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side=tk.LEFT)
        
        # Bind Enter key to submit
        self.parent.bind('<Return>', lambda event: self.submit())
        
        # Focus on email field
        self.email_entry.focus()
        
    def submit(self):
        """Handle password recovery request"""
        email = self.email_entry.get().strip()
        
        if not email:
            messagebox.showerror("Error", "Please enter your email address")
            return
            
        # Check if email is valid (basic check)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        # Check if user exists
        user = self.user_dao.get_user_by_email(email)
        
        if user:
            # In a real application, this would send an email with a reset link
            messagebox.showinfo("Success", 
                               f"Password reset instructions have been sent to {email}\n\n"
                               "In a real application, an email would be sent with reset instructions.")
        else:
            messagebox.showerror("Error", "No account found with that email address")
    
    def cancel(self):
        """Cancel and return to login"""
        self.parent.destroy()
        if self.return_callback:
            self.return_callback()