"""
Customer Panel
Allows admins to manage customer records
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.customer_dao import CustomerDAO, Customer


class CustomerPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.customer_dao = CustomerDAO()
        self.current_customer = None
        
        self.setup_ui()
        self.refresh_customer_list()
        
    def setup_ui(self):
        """Setup the customer management interface"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Customer list
        left_frame = ttk.LabelFrame(main_container, text="Customers", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Customer list
        columns = ('ID', 'First Name', 'Last Name', 'Email', 'Phone')
        self.customer_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=100)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.customer_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        
        # Right side - Customer details and actions
        right_frame = ttk.LabelFrame(main_container, text="Customer Details", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Customer details form
        ttk.Label(right_frame, text="First Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(right_frame, textvariable=self.first_name_var, width=25)
        self.first_name_entry.grid(row=0, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Last Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(right_frame, textvariable=self.last_name_var, width=25)
        self.last_name_entry.grid(row=1, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(right_frame, textvariable=self.email_var, width=25)
        self.email_entry.grid(row=2, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(right_frame, textvariable=self.phone_var, width=25)
        self.phone_entry.grid(row=3, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Address:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(right_frame, textvariable=self.address_var, width=25)
        self.address_entry.grid(row=4, column=1, pady=2, padx=(5, 0))
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        self.add_btn = ttk.Button(btn_frame, text="Add Customer", command=self.add_customer)
        self.add_btn.pack(fill=tk.X, pady=2)
        
        self.update_btn = ttk.Button(btn_frame, text="Update Customer", command=self.update_customer, state=tk.DISABLED)
        self.update_btn.pack(fill=tk.X, pady=2)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete Customer", command=self.delete_customer, state=tk.DISABLED)
        self.delete_btn.pack(fill=tk.X, pady=2)
        
        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_form)
        self.clear_btn.pack(fill=tk.X, pady=2)
    
    def refresh_customer_list(self):
        """Refresh the customer list from the database"""
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Get customers from DAO
        customers = self.customer_dao.get_all_customers()
        
        # Insert customers into treeview
        for customer in customers:
            self.customer_tree.insert('', tk.END, values=(
                customer.id, 
                customer.first_name, 
                customer.last_name, 
                customer.email, 
                customer.phone
            ))
    
    def on_customer_select(self, event):
        """Handle customer selection in the treeview"""
        selection = self.customer_tree.selection()
        if selection:
            item = self.customer_tree.item(selection[0])
            customer_id = item['values'][0]
            
            # Get full customer details from DAO
            self.current_customer = self.customer_dao.get_customer_by_id(customer_id)
            
            if self.current_customer:
                self.first_name_var.set(self.current_customer.first_name)
                self.last_name_var.set(self.current_customer.last_name)
                self.email_var.set(self.current_customer.email)
                self.phone_var.set(self.current_customer.phone)
                self.address_var.set(self.current_customer.address)
                
                # Enable update/delete buttons
                self.update_btn.config(state=tk.NORMAL)
                self.delete_btn.config(state=tk.NORMAL)
                self.add_btn.config(state=tk.DISABLED)
        else:
            self.clear_form()
    
    def on_search_change(self, event):
        """Handle search input changes"""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Get all customers and filter
        all_customers = self.customer_dao.get_all_customers()
        filtered_customers = [
            customer for customer in all_customers 
            if search_term in customer.first_name.lower() or 
               search_term in customer.last_name.lower() or 
               search_term in customer.email.lower() or
               (customer.phone and search_term in customer.phone.lower()) or
               (customer.address and search_term in customer.address.lower())
        ]
        
        # Insert filtered customers into treeview
        for customer in filtered_customers:
            self.customer_tree.insert('', tk.END, values=(
                customer.id, 
                customer.first_name, 
                customer.last_name, 
                customer.email, 
                customer.phone
            ))
    
    def add_customer(self):
        """Add a new customer"""
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        
        if not first_name or not last_name or not email:
            messagebox.showerror("Error", "Please fill in at least first name, last name, and email")
            return
        
        # Check if email is valid (basic check)
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
        
        # Try to create customer
        if self.customer_dao.create_customer(customer):
            messagebox.showinfo("Success", "Customer created successfully")
            self.refresh_customer_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Email already exists")
    
    def update_customer(self):
        """Update the selected customer"""
        if not self.current_customer:
            return
        
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        
        if not first_name or not last_name or not email:
            messagebox.showerror("Error", "Please fill in at least first name, last name, and email")
            return
        
        # Check if email is valid (basic check)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        # Update customer object
        self.current_customer.first_name = first_name
        self.current_customer.last_name = last_name
        self.current_customer.email = email
        self.current_customer.phone = phone
        self.current_customer.address = address
        
        # Try to update customer
        if self.customer_dao.update_customer(self.current_customer):
            messagebox.showinfo("Success", "Customer updated successfully")
            self.refresh_customer_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update customer")
    
    def delete_customer(self):
        """Delete the selected customer"""
        if not self.current_customer:
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete customer {self.current_customer.first_name} {self.current_customer.last_name}?"):
            if self.customer_dao.delete_customer(self.current_customer.id):
                messagebox.showinfo("Success", "Customer deleted successfully")
                self.refresh_customer_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to delete customer")
    
    def clear_form(self):
        """Clear the customer details form"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.current_customer = None
        
        # Clear selection in treeview
        self.customer_tree.selection_remove(self.customer_tree.selection())
        
        # Disable update/delete buttons, enable add button
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.add_btn.config(state=tk.NORMAL)