"""
Purchase Panel
Handles product purchases
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.product_dao import ProductDAO, Product
from dao.customer_dao import CustomerDAO
from dao.borrowing_dao import BorrowingDAO, Borrowing
from service.session_manager import SessionManager
from datetime import datetime


class PurchasePanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.product_dao = ProductDAO()
        self.customer_dao = CustomerDAO()
        self.borrowing_dao = BorrowingDAO()
        self.session_manager = SessionManager()
        
        self.setup_ui()
        self.refresh_product_list()
        
    def setup_ui(self):
        """Setup the purchase interface"""
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Product Purchases", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Product search
        ttk.Label(search_frame, text="Search Products:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Product list
        columns = ('ID', 'Name', 'Category', 'Price', 'Available')
        self.product_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        for col in columns:
            self.product_tree.heading(col, text=col)
            if col == 'Name':
                self.product_tree.column(col, width=200)
            else:
                self.product_tree.column(col, width=100)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 20))
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Purchase details frame
        details_frame = ttk.LabelFrame(main_frame, text="Purchase Details", padding=15)
        details_frame.pack(fill=tk.X)
        
        # Customer ID
        ttk.Label(details_frame, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.customer_id_var = tk.StringVar()
        self.customer_id_entry = ttk.Entry(details_frame, textvariable=self.customer_id_var, width=20)
        self.customer_id_entry.grid(row=0, column=1, pady=5)
        
        # Product ID (read-only, populated when selecting product)
        ttk.Label(details_frame, text="Product ID:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.product_id_var = tk.StringVar()
        self.product_id_entry = ttk.Entry(details_frame, textvariable=self.product_id_var, width=20, state="readonly")
        self.product_id_entry.grid(row=1, column=1, pady=5)
        
        # Quantity
        ttk.Label(details_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_spinbox = ttk.Spinbox(details_frame, from_=1, to=999, textvariable=self.quantity_var, width=18)
        self.quantity_spinbox.grid(row=2, column=1, pady=5)
        
        # Due Date
        ttk.Label(details_frame, text="Due Date (optional):").grid(row=3, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.due_date_var = tk.StringVar()
        self.due_date_entry = ttk.Entry(details_frame, textvariable=self.due_date_var, width=20)
        self.due_date_entry.grid(row=3, column=1, pady=5)
        
        # Notes
        ttk.Label(details_frame, text="Notes:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.notes_var = tk.StringVar()
        self.notes_entry = ttk.Entry(details_frame, textvariable=self.notes_var, width=50)
        self.notes_entry.grid(row=4, column=1, pady=5, sticky=tk.W+tk.E)
        
        # Configure column to expand
        details_frame.columnconfigure(1, weight=1)
        
        # Purchase button
        purchase_btn = ttk.Button(main_frame, text="Process Purchase", command=self.process_purchase)
        purchase_btn.pack(pady=15)
        
        # Bind selection event
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
    
    def refresh_product_list(self):
        """Refresh the product list from the database"""
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get products from DAO
        products = self.product_dao.get_all_products()
        
        # Insert products into treeview
        for product in products:
            if product.quantity_available > 0:  # Only show products that are available
                self.product_tree.insert('', tk.END, values=(
                    product.id, 
                    product.name, 
                    product.category, 
                    product.price, 
                    product.quantity_available
                ))
    
    def on_search_change(self, event):
        """Handle search input changes"""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get all products and filter
        all_products = self.product_dao.get_all_products()
        filtered_products = [
            product for product in all_products 
            if (search_term in product.name.lower() or 
                search_term in product.category.lower() or 
                search_term in str(product.price)) and
                product.quantity_available > 0  # Only show available products
        ]
        
        # Insert filtered products into treeview
        for product in filtered_products:
            self.product_tree.insert('', tk.END, values=(
                product.id, 
                product.name, 
                product.category, 
                product.price, 
                product.quantity_available
            ))
    
    def on_product_select(self, event):
        """Handle product selection in the treeview"""
        selection = self.product_tree.selection()
        if selection:
            item = self.product_tree.item(selection[0])
            product_id = item['values'][0]
            self.product_id_var.set(str(product_id))
    
    def process_purchase(self):
        """Process the purchase of a product"""
        # Get customer ID
        customer_id_str = self.customer_id_var.get()
        product_id_str = self.product_id_var.get()
        quantity = self.quantity_var.get()
        
        if not customer_id_str:
            messagebox.showerror("Error", "Please enter a customer ID")
            return
        
        if not product_id_str:
            messagebox.showerror("Error", "Please select a product to purchase")
            return
        
        try:
            customer_id = int(customer_id_str)
            product_id = int(product_id_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid customer and product IDs")
            return
        
        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0")
            return
        
        # Verify customer exists
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            messagebox.showerror("Error", "Customer not found")
            return
        
        # Get the product
        product = self.product_dao.get_product_by_id(product_id)
        if not product:
            messagebox.showerror("Error", "Product not found")
            return
        
        if product.quantity_available < quantity:
            messagebox.showerror("Error", f"Only {product.quantity_available} units available")
            return
        
        # Create borrowing record (for tracking the purchase/loan)
        current_user = self.session_manager.get_current_user()
        borrowing = Borrowing(
            customer_id=customer_id,
            product_id=product_id,
            borrowed_by_user_id=current_user.id,
            due_date=self.due_date_var.get() or None,
            notes=self.notes_var.get() or "",
            status="borrowed"  # Initially borrowed, will be returned later
        )
        
        # Process the borrowing
        if self.borrowing_dao.create_borrowing(borrowing):
            # Update product quantity
            product.quantity_available -= quantity
            self.product_dao.update_product(product)
            
            messagebox.showinfo("Success", f"Purchase processed successfully!\nProduct: {product.name}\nQuantity: {quantity}")
            
            # Clear form and refresh the list
            self.customer_id_var.set("")
            self.product_id_var.set("")
            self.quantity_var.set(1)
            self.due_date_var.set("")
            self.notes_var.set("")
            
            self.refresh_product_list()
        else:
            messagebox.showerror("Error", "Failed to process purchase")