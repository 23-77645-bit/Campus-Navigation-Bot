"""
Borrowing History Panel
Shows borrowing history for customers
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.borrowing_dao import BorrowingDAO, Borrowing
from dao.customer_dao import CustomerDAO
from dao.product_dao import ProductDAO
from dao.user_dao import UserDAO


class BorrowingHistoryPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.borrowing_dao = BorrowingDAO()
        self.customer_dao = CustomerDAO()
        self.product_dao = ProductDAO()
        self.user_dao = UserDAO()
        
        self.setup_ui()
        self.refresh_borrowing_history()
        
    def setup_ui(self):
        """Setup the borrowing history interface"""
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Borrowing History", font=("Arial", 16, "bold"))
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
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_borrowings)
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(search_frame, text="Refresh All", command=self.refresh_borrowing_history)
        refresh_btn.pack(side=tk.LEFT)
        
        # Borrowing history list
        columns = ('ID', 'Customer', 'Product', 'Borrowed By', 'Date', 'Due Date', 'Status')
        self.borrowing_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.borrowing_tree.heading(col, text=col)
            if col in ['Customer', 'Product']:
                self.borrowing_tree.column(col, width=120)
            else:
                self.borrowing_tree.column(col, width=80)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.borrowing_tree.yview)
        self.borrowing_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.borrowing_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def refresh_borrowing_history(self):
        """Refresh the borrowing history list from the database"""
        # Clear existing items
        for item in self.borrowing_tree.get_children():
            self.borrowing_tree.delete(item)
        
        # Get all borrowings from DAO
        borrowings = self.borrowing_dao.get_all_borrowings()
        
        # Insert borrowings into treeview with customer and product names
        self.insert_borrowings_to_tree(borrowings)
    
    def search_borrowings(self):
        """Search borrowings by customer ID"""
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
        
        # Get borrowings for this customer
        borrowings = self.borrowing_dao.get_borrowings_by_customer(customer_id)
        
        # Clear existing items
        for item in self.borrowing_tree.get_children():
            self.borrowing_tree.delete(item)
        
        # Insert borrowings into treeview with customer and product names
        self.insert_borrowings_to_tree(borrowings)
    
    def insert_borrowings_to_tree(self, borrowings):
        """Insert borrowings into the treeview"""
        for borrowing in borrowings:
            # Get customer name
            customer = self.customer_dao.get_customer_by_id(borrowing.customer_id)
            customer_name = f"{customer.first_name} {customer.last_name}" if customer else "Unknown"
            
            # Get product name
            product = self.product_dao.get_product_by_id(borrowing.product_id)
            product_name = product.name if product else "Unknown"
            
            # Get user name who borrowed
            user = self.user_dao.get_user_by_username(borrowing.borrowed_by_user_id)
            user_name = user.username if user else "Unknown"
            
            self.borrowing_tree.insert('', tk.END, values=(
                borrowing.id, 
                customer_name, 
                product_name, 
                user_name, 
                borrowing.borrowed_date, 
                borrowing.due_date or "N/A",
                borrowing.status
            ))