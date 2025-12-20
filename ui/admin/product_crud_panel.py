"""
Product CRUD Panel
Allows admins to manage products
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.product_dao import ProductDAO, Product


class ProductCRUDPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.product_dao = ProductDAO()
        self.current_product = None
        
        self.setup_ui()
        self.refresh_product_list()
        
    def setup_ui(self):
        """Setup the product management interface"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Product list
        left_frame = ttk.LabelFrame(main_container, text="Products", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Product list
        columns = ('ID', 'Name', 'Category', 'Price', 'Available')
        self.product_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=100)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Right side - Product details and actions
        right_frame = ttk.LabelFrame(main_container, text="Product Details", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Product details form
        ttk.Label(right_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(right_frame, textvariable=self.name_var, width=25)
        self.name_entry.grid(row=0, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(right_frame, textvariable=self.description_var, width=25)
        self.description_entry.grid(row=1, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.category_var = tk.StringVar()
        self.category_entry = ttk.Entry(right_frame, textvariable=self.category_var, width=25)
        self.category_entry.grid(row=2, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Price:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.price_var = tk.DoubleVar()
        self.price_entry = ttk.Entry(right_frame, textvariable=self.price_var, width=25)
        self.price_entry.grid(row=3, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Available:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.quantity_var = tk.IntVar()
        self.quantity_entry = ttk.Entry(right_frame, textvariable=self.quantity_var, width=25)
        self.quantity_entry.grid(row=4, column=1, pady=2, padx=(5, 0))
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        self.add_btn = ttk.Button(btn_frame, text="Add Product", command=self.add_product)
        self.add_btn.pack(fill=tk.X, pady=2)
        
        self.update_btn = ttk.Button(btn_frame, text="Update Product", command=self.update_product, state=tk.DISABLED)
        self.update_btn.pack(fill=tk.X, pady=2)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete Product", command=self.delete_product, state=tk.DISABLED)
        self.delete_btn.pack(fill=tk.X, pady=2)
        
        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_form)
        self.clear_btn.pack(fill=tk.X, pady=2)
    
    def refresh_product_list(self):
        """Refresh the product list from the database"""
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get products from DAO
        products = self.product_dao.get_all_products()
        
        # Insert products into treeview
        for product in products:
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
            
            # Get full product details from DAO
            self.current_product = self.product_dao.get_product_by_id(product_id)
            
            if self.current_product:
                self.name_var.set(self.current_product.name)
                self.description_var.set(self.current_product.description)
                self.category_var.set(self.current_product.category)
                self.price_var.set(self.current_product.price)
                self.quantity_var.set(self.current_product.quantity_available)
                
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
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get all products and filter
        all_products = self.product_dao.get_all_products()
        filtered_products = [
            product for product in all_products 
            if search_term in product.name.lower() or 
               search_term in product.category.lower() or 
               search_term in product.description.lower()
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
    
    def add_product(self):
        """Add a new product"""
        name = self.name_var.get().strip()
        description = self.description_var.get().strip()
        category = self.category_var.get().strip()
        try:
            price = float(self.price_var.get()) if self.price_var.get() else 0.0
            quantity = int(self.quantity_var.get()) if self.quantity_var.get() else 0
        except ValueError:
            messagebox.showerror("Error", "Price and quantity must be valid numbers")
            return
        
        if not name or category == "":
            messagebox.showerror("Error", "Please fill in at least the name and category")
            return
        
        # Create product object
        product = Product(
            name=name, 
            description=description, 
            category=category, 
            price=price, 
            quantity_available=quantity
        )
        
        # Try to create product
        if self.product_dao.create_product(product):
            messagebox.showinfo("Success", "Product created successfully")
            self.refresh_product_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to create product")
    
    def update_product(self):
        """Update the selected product"""
        if not self.current_product:
            return
        
        name = self.name_var.get().strip()
        description = self.description_var.get().strip()
        category = self.category_var.get().strip()
        try:
            price = float(self.price_var.get()) if self.price_var.get() else 0.0
            quantity = int(self.quantity_var.get()) if self.quantity_var.get() else 0
        except ValueError:
            messagebox.showerror("Error", "Price and quantity must be valid numbers")
            return
        
        if not name or category == "":
            messagebox.showerror("Error", "Please fill in at least the name and category")
            return
        
        # Update product object
        self.current_product.name = name
        self.current_product.description = description
        self.current_product.category = category
        self.current_product.price = price
        self.current_product.quantity_available = quantity
        
        # Try to update product
        if self.product_dao.update_product(self.current_product):
            messagebox.showinfo("Success", "Product updated successfully")
            self.refresh_product_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update product")
    
    def delete_product(self):
        """Delete the selected product"""
        if not self.current_product:
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product {self.current_product.name}?"):
            if self.product_dao.delete_product(self.current_product.id):
                messagebox.showinfo("Success", "Product deleted successfully")
                self.refresh_product_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to delete product")
    
    def clear_form(self):
        """Clear the product details form"""
        self.name_var.set("")
        self.description_var.set("")
        self.category_var.set("")
        self.price_var.set(0.0)
        self.quantity_var.set(0)
        self.current_product = None
        
        # Clear selection in treeview
        self.product_tree.selection_remove(self.product_tree.selection())
        
        # Disable update/delete buttons, enable add button
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.add_btn.config(state=tk.NORMAL)