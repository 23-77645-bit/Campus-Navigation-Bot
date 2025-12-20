"""
Borrowing Report Panel
Shows borrowing reports and allows managing borrowings
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.borrowing_dao import BorrowingDAO, Borrowing
from dao.customer_dao import CustomerDAO
from dao.product_dao import ProductDAO
from dao.user_dao import UserDAO
from datetime import datetime


class BorrowingReportPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.borrowing_dao = BorrowingDAO()
        self.customer_dao = CustomerDAO()
        self.product_dao = ProductDAO()
        self.user_dao = UserDAO()
        self.current_borrowing = None
        
        self.setup_ui()
        self.refresh_borrowing_list()
        
    def setup_ui(self):
        """Setup the borrowing report interface"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Borrowing list
        left_frame = ttk.LabelFrame(main_container, text="Borrowing Records", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Borrowing list
        columns = ('ID', 'Customer', 'Product', 'Borrowed By', 'Date', 'Status')
        self.borrowing_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.borrowing_tree.heading(col, text=col)
            self.borrowing_tree.column(col, width=100)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.borrowing_tree.yview)
        self.borrowing_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.borrowing_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.borrowing_tree.bind('<<TreeviewSelect>>', self.on_borrowing_select)
        
        # Right side - Borrowing details and actions
        right_frame = ttk.LabelFrame(main_container, text="Borrowing Details", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Borrowing details form
        ttk.Label(right_frame, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.customer_id_var = tk.IntVar()
        self.customer_id_entry = ttk.Entry(right_frame, textvariable=self.customer_id_var, width=25)
        self.customer_id_entry.grid(row=0, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Product ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.product_id_var = tk.IntVar()
        self.product_id_entry = ttk.Entry(right_frame, textvariable=self.product_id_var, width=25)
        self.product_id_entry.grid(row=1, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Borrowed By (User ID):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.borrowed_by_id_var = tk.IntVar()
        self.borrowed_by_id_entry = ttk.Entry(right_frame, textvariable=self.borrowed_by_id_var, width=25)
        self.borrowed_by_id_entry.grid(row=2, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Borrowed Date:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.borrowed_date_var = tk.StringVar()
        self.borrowed_date_entry = ttk.Entry(right_frame, textvariable=self.borrowed_date_var, width=25)
        self.borrowed_date_entry.grid(row=3, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Due Date:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.due_date_var = tk.StringVar()
        self.due_date_entry = ttk.Entry(right_frame, textvariable=self.due_date_var, width=25)
        self.due_date_entry.grid(row=4, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Status:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(right_frame, textvariable=self.status_var, 
                                        values=["borrowed", "returned", "overdue"], state="readonly", width=22)
        self.status_combo.grid(row=5, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Notes:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.notes_var = tk.StringVar()
        self.notes_entry = ttk.Entry(right_frame, textvariable=self.notes_var, width=25)
        self.notes_entry.grid(row=6, column=1, pady=2, padx=(5, 0))
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=15)
        
        self.add_btn = ttk.Button(btn_frame, text="Add Borrowing", command=self.add_borrowing)
        self.add_btn.pack(fill=tk.X, pady=2)
        
        self.update_btn = ttk.Button(btn_frame, text="Update Borrowing", command=self.update_borrowing, state=tk.DISABLED)
        self.update_btn.pack(fill=tk.X, pady=2)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete Borrowing", command=self.delete_borrowing, state=tk.DISABLED)
        self.delete_btn.pack(fill=tk.X, pady=2)
        
        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_form)
        self.clear_btn.pack(fill=tk.X, pady=2)
    
    def refresh_borrowing_list(self):
        """Refresh the borrowing list from the database"""
        # Clear existing items
        for item in self.borrowing_tree.get_children():
            self.borrowing_tree.delete(item)
        
        # Get borrowings from DAO
        borrowings = self.borrowing_dao.get_all_borrowings()
        
        # Insert borrowings into treeview with customer and product names
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
                borrowing.status
            ))
    
    def on_borrowing_select(self, event):
        """Handle borrowing selection in the treeview"""
        selection = self.borrowing_tree.selection()
        if selection:
            item = self.borrowing_tree.item(selection[0])
            borrowing_id = item['values'][0]
            
            # Get full borrowing details from DAO
            self.current_borrowing = self.borrowing_dao.get_borrowing_by_id(borrowing_id)
            
            if self.current_borrowing:
                self.customer_id_var.set(self.current_borrowing.customer_id or 0)
                self.product_id_var.set(self.current_borrowing.product_id or 0)
                self.borrowed_by_id_var.set(self.current_borrowing.borrowed_by_user_id or 0)
                self.borrowed_date_var.set(self.current_borrowing.borrowed_date or "")
                self.due_date_var.set(self.current_borrowing.due_date or "")
                self.status_var.set(self.current_borrowing.status or "borrowed")
                self.notes_var.set(self.current_borrowing.notes or "")
                
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
        for item in self.borrowing_tree.get_children():
            self.borrowing_tree.delete(item)
        
        # Get all borrowings and filter
        all_borrowings = self.borrowing_dao.get_all_borrowings()
        filtered_borrowings = []
        
        for borrowing in all_borrowings:
            # Get related data for search
            customer = self.customer_dao.get_customer_by_id(borrowing.customer_id)
            customer_name = f"{customer.first_name} {customer.last_name}".lower() if customer else ""
            
            product = self.product_dao.get_product_by_id(borrowing.product_id)
            product_name = product.name.lower() if product else ""
            
            if (search_term in str(borrowing.id) or 
                search_term in customer_name or 
                search_term in product_name or
                search_term in borrowing.status.lower() or
                search_term in str(borrowing.borrowed_date).lower()):
                filtered_borrowings.append(borrowing)
        
        # Insert filtered borrowings into treeview
        for borrowing in filtered_borrowings:
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
                borrowing.status
            ))
    
    def add_borrowing(self):
        """Add a new borrowing record"""
        try:
            customer_id = int(self.customer_id_var.get())
            product_id = int(self.product_id_var.get())
            borrowed_by_user_id = int(self.borrowed_by_id_var.get())
            borrowed_date = self.borrowed_date_var.get() or datetime.now().isoformat()
            due_date = self.due_date_var.get()
            status = self.status_var.get() or "borrowed"
            notes = self.notes_var.get()
        except ValueError:
            messagebox.showerror("Error", "Customer ID, Product ID, and Borrowed By User ID must be valid numbers")
            return
        
        if not customer_id or not product_id or not borrowed_by_user_id:
            messagebox.showerror("Error", "Please fill in customer, product, and user IDs")
            return
        
        # Check if customer and product exist
        customer = self.customer_dao.get_customer_by_id(customer_id)
        product = self.product_dao.get_product_by_id(product_id)
        user = self.user_dao.get_user_by_username(borrowed_by_user_id)
        
        if not customer:
            messagebox.showerror("Error", "Invalid customer ID")
            return
        
        if not product:
            messagebox.showerror("Error", "Invalid product ID")
            return
            
        if not user:
            messagebox.showerror("Error", "Invalid user ID")
            return
        
        # Create borrowing object
        borrowing = Borrowing(
            customer_id=customer_id, 
            product_id=product_id, 
            borrowed_by_user_id=borrowed_by_user_id, 
            borrowed_date=borrowed_date,
            due_date=due_date,
            status=status,
            notes=notes
        )
        
        # Try to create borrowing
        if self.borrowing_dao.create_borrowing(borrowing):
            messagebox.showinfo("Success", "Borrowing record created successfully")
            self.refresh_borrowing_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to create borrowing record")
    
    def update_borrowing(self):
        """Update the selected borrowing record"""
        if not self.current_borrowing:
            return
        
        try:
            customer_id = int(self.customer_id_var.get())
            product_id = int(self.product_id_var.get())
            borrowed_by_user_id = int(self.borrowed_by_id_var.get())
            borrowed_date = self.borrowed_date_var.get()
            due_date = self.due_date_var.get()
            status = self.status_var.get()
            notes = self.notes_var.get()
        except ValueError:
            messagebox.showerror("Error", "Customer ID, Product ID, and Borrowed By User ID must be valid numbers")
            return
        
        if not customer_id or not product_id or not borrowed_by_user_id:
            messagebox.showerror("Error", "Please fill in customer, product, and user IDs")
            return
        
        # Update borrowing object
        self.current_borrowing.customer_id = customer_id
        self.current_borrowing.product_id = product_id
        self.current_borrowing.borrowed_by_user_id = borrowed_by_user_id
        self.current_borrowing.borrowed_date = borrowed_date
        self.current_borrowing.due_date = due_date
        self.current_borrowing.status = status
        self.current_borrowing.notes = notes
        
        # Try to update borrowing
        if self.borrowing_dao.update_borrowing(self.current_borrowing):
            messagebox.showinfo("Success", "Borrowing record updated successfully")
            self.refresh_borrowing_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update borrowing record")
    
    def delete_borrowing(self):
        """Delete the selected borrowing record"""
        if not self.current_borrowing:
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete borrowing record {self.current_borrowing.id}?"):
            if self.borrowing_dao.delete_borrowing(self.current_borrowing.id):
                messagebox.showinfo("Success", "Borrowing record deleted successfully")
                self.refresh_borrowing_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to delete borrowing record")
    
    def clear_form(self):
        """Clear the borrowing details form"""
        self.customer_id_var.set(0)
        self.product_id_var.set(0)
        self.borrowed_by_id_var.set(0)
        self.borrowed_date_var.set("")
        self.due_date_var.set("")
        self.status_var.set("borrowed")
        self.notes_var.set("")
        self.current_borrowing = None
        
        # Clear selection in treeview
        self.borrowing_tree.selection_remove(self.borrowing_tree.selection())
        
        # Disable update/delete buttons, enable add button
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.add_btn.config(state=tk.NORMAL)