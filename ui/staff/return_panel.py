"""
Return Panel
Handles product returns
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.borrowing_dao import BorrowingDAO
from dao.product_dao import ProductDAO
from dao.customer_dao import CustomerDAO
from service.session_manager import SessionManager
from datetime import datetime


class ReturnPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.borrowing_dao = BorrowingDAO()
        self.product_dao = ProductDAO()
        self.customer_dao = CustomerDAO()
        self.session_manager = SessionManager()
        
        self.setup_ui()
        self.refresh_active_borrowings()
        
        # Bind selection event after treeview is created
        self.borrowing_tree.bind('<<TreeviewSelect>>', self.on_borrowing_select)
        
    def setup_ui(self):
        """Setup the return interface"""
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Product Returns", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Customer search
        ttk.Label(search_frame, text="Search by Customer ID:").pack(side=tk.LEFT, padx=(0, 5))
        self.customer_id_var = tk.StringVar()
        self.customer_id_entry = ttk.Entry(search_frame, textvariable=self.customer_id_var, width=15)
        self.customer_id_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Search button
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_returns)
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(search_frame, text="Refresh Active", command=self.refresh_active_borrowings)
        refresh_btn.pack(side=tk.LEFT)
        
        # Active borrowings list
        columns = ('ID', 'Customer', 'Product', 'Borrowed Date', 'Due Date')
        self.borrowing_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=10)
        
        # Define headings
        for col in columns:
            self.borrowing_tree.heading(col, text=col)
            if col in ['Customer', 'Product']:
                self.borrowing_tree.column(col, width=150)
            else:
                self.borrowing_tree.column(col, width=100)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.borrowing_tree.yview)
        self.borrowing_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 20))
        self.borrowing_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Return details frame
        details_frame = ttk.LabelFrame(main_frame, text="Return Details", padding=15)
        details_frame.pack(fill=tk.X)
        
        # Borrowing ID
        ttk.Label(details_frame, text="Borrowing ID:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.borrowing_id_var = tk.StringVar()
        self.borrowing_id_entry = ttk.Entry(details_frame, textvariable=self.borrowing_id_var, width=20, state="readonly")
        self.borrowing_id_entry.grid(row=0, column=1, pady=5)
        
        # Notes
        ttk.Label(details_frame, text="Notes:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.notes_var = tk.StringVar()
        self.notes_entry = ttk.Entry(details_frame, textvariable=self.notes_var, width=50)
        self.notes_entry.grid(row=1, column=1, pady=5, sticky=tk.W+tk.E)
        
        # Configure column to expand
        details_frame.columnconfigure(1, weight=1)
        
        # Return button
        return_btn = ttk.Button(main_frame, text="Process Return", command=self.process_return)
        return_btn.pack(pady=15)
    
    def refresh_active_borrowings(self):
        """Refresh the active borrowings list from the database"""
        # Clear existing items
        for item in self.borrowing_tree.get_children():
            self.borrowing_tree.delete(item)
        
        # Get active borrowings from DAO
        borrowings = self.borrowing_dao.get_active_borrowings()
        
        # Insert borrowings into treeview with customer and product names
        for borrowing in borrowings:
            # Get customer name
            customer = self.customer_dao.get_customer_by_id(borrowing.customer_id)
            customer_name = f"{customer.first_name} {customer.last_name}" if customer else "Unknown"
            
            # Get product name
            product = self.product_dao.get_product_by_id(borrowing.product_id)
            product_name = product.name if product else "Unknown"
            
            self.borrowing_tree.insert('', tk.END, values=(
                borrowing.id, 
                customer_name, 
                product_name, 
                borrowing.borrowed_date, 
                borrowing.due_date or "N/A"
            ))
    
    def search_returns(self):
        """Search returns by customer ID"""
        try:
            customer_id = int(self.customer_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid customer ID")
            return
        
        # Get customer to verify it exists
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            messagebox.showerror("Error", "Customer not found")
            return
        
        # Get active borrowings for this customer
        borrowings = self.borrowing_dao.get_borrowings_by_customer(customer_id)
        # Filter to only active (not returned) borrowings
        active_borrowings = [b for b in borrowings if b.status == 'borrowed']
        
        # Clear existing items
        for item in self.borrowing_tree.get_children():
            self.borrowing_tree.delete(item)
        
        # Insert borrowings into treeview with customer and product names
        for borrowing in active_borrowings:
            # Get customer name
            customer = self.customer_dao.get_customer_by_id(borrowing.customer_id)
            customer_name = f"{customer.first_name} {customer.last_name}" if customer else "Unknown"
            
            # Get product name
            product = self.product_dao.get_product_by_id(borrowing.product_id)
            product_name = product.name if product else "Unknown"
            
            self.borrowing_tree.insert('', tk.END, values=(
                borrowing.id, 
                customer_name, 
                product_name, 
                borrowing.borrowed_date, 
                borrowing.due_date or "N/A"
            ))
    
    def on_borrowing_select(self, event):
        """Handle borrowing selection in the treeview"""
        selection = self.borrowing_tree.selection()
        if selection:
            item = self.borrowing_tree.item(selection[0])
            borrowing_id = item['values'][0]
            self.borrowing_id_var.set(str(borrowing_id))
    
    def process_return(self):
        """Process the return of a product"""
        borrowing_id_str = self.borrowing_id_var.get()
        
        if not borrowing_id_str:
            messagebox.showerror("Error", "Please select a borrowing to return")
            return
        
        try:
            borrowing_id = int(borrowing_id_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid borrowing ID")
            return
        
        # Get the borrowing record
        borrowing = self.borrowing_dao.get_borrowing_by_id(borrowing_id)
        if not borrowing:
            messagebox.showerror("Error", "Borrowing record not found")
            return
        
        if borrowing.status != 'borrowed':
            messagebox.showerror("Error", "This item has already been returned")
            return
        
        # Update the borrowing record to mark as returned
        borrowing.status = 'returned'
        borrowing.returned_date = datetime.now().isoformat()
        borrowing.notes = self.notes_var.get() or borrowing.notes
        
        if self.borrowing_dao.update_borrowing(borrowing):
            # Update the product's available quantity
            product = self.product_dao.get_product_by_id(borrowing.product_id)
            if product:
                product.quantity_available += 1
                self.product_dao.update_product(product)
            
            messagebox.showinfo("Success", f"Product returned successfully!\nBorrowing ID: {borrowing_id}")
            
            # Clear form and refresh the list
            self.borrowing_id_var.set("")
            self.notes_var.set("")
            self.refresh_active_borrowings()
        else:
            messagebox.showerror("Error", "Failed to process return")
    
    def __init__(self, parent):
        super().__init__(parent)
        self.borrowing_dao = BorrowingDAO()
        self.product_dao = ProductDAO()
        self.customer_dao = CustomerDAO()
        self.session_manager = SessionManager()
        
        # Bind selection event
        self.borrowing_tree.bind('<<TreeviewSelect>>', self.on_borrowing_select)
        
        self.setup_ui()
        self.refresh_active_borrowings()