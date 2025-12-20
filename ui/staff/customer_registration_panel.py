"""
Customer Registration Panel
Allows staff to register new customers
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.customer_dao import CustomerDAO, Customer


class CustomerRegistrationPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.customer_dao = CustomerDAO()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the customer registration interface"""
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Customer Registration", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Customer details form
        form_frame = ttk.LabelFrame(main_frame, text="Customer Information", padding=15)
        form_frame.pack(fill=tk.X, pady=(0, 15))
        
        # First name
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(form_frame, textvariable=self.first_name_var, width=30)
        self.first_name_entry.grid(row=0, column=1, pady=5)
        
        # Last name
        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(form_frame, textvariable=self.last_name_var, width=30)
        self.last_name_entry.grid(row=1, column=1, pady=5)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=2, column=1, pady=5)
        
        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(form_frame, textvariable=self.phone_var, width=30)
        self.phone_entry.grid(row=3, column=1, pady=5)
        
        # Address
        ttk.Label(form_frame, text="Address:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(form_frame, textvariable=self.address_var, width=30)
        self.address_entry.grid(row=4, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        register_btn = ttk.Button(button_frame, text="Register Customer", command=self.register_customer)
        register_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Clear Form", command=self.clear_form)
        clear_btn.pack(side=tk.LEFT)
        
        # Bind Enter key to register
        self.bind('<Return>', lambda event: self.register_customer())
        self.focus_set()
    
    def register_customer(self):
        """Register a new customer"""
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        
        # Validation
        if not first_name or not last_name or not email:
            messagebox.showerror("Error", "Please fill in first name, last name, and email")
            return
        
        # Basic email validation
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        # Create customer object
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address
        )
        
        # Try to register customer
        if self.customer_dao.create_customer(customer):
            messagebox.showinfo("Success", f"Customer {first_name} {last_name} registered successfully!")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Email already exists")
    
    def clear_form(self):
        """Clear all form fields"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        
        # Focus on first field
        self.first_name_entry.focus()