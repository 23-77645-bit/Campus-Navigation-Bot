"""
User Management Panel
Allows admins to manage user accounts
"""
import tkinter as tk
from tkinter import ttk, messagebox
from dao.user_dao import UserDAO
from model.user import User


class UserManagementPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_dao = UserDAO()
        self.current_user = None
        
        self.setup_ui()
        self.refresh_user_list()
        
    def setup_ui(self):
        """Setup the user management interface"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - User list
        left_frame = ttk.LabelFrame(main_container, text="Users", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # User list
        columns = ('ID', 'Username', 'Email', 'Role')
        self.user_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=100)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.user_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        
        # Right side - User details and actions
        right_frame = ttk.LabelFrame(main_container, text="User Details", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # User details form
        ttk.Label(right_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(right_frame, textvariable=self.username_var, width=25)
        self.username_entry.grid(row=0, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(right_frame, textvariable=self.email_var, width=25)
        self.email_entry.grid(row=1, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(right_frame, text="Role:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.role_var = tk.StringVar()
        self.role_combo = ttk.Combobox(right_frame, textvariable=self.role_var, 
                                      values=["admin", "staff"], state="readonly", width=22)
        self.role_combo.grid(row=2, column=1, pady=2, padx=(5, 0))
        
        # Password field (only for new users or password changes)
        ttk.Label(right_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(right_frame, textvariable=self.password_var, width=25, show="*")
        self.password_entry.grid(row=3, column=1, pady=2, padx=(5, 0))
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        self.add_btn = ttk.Button(btn_frame, text="Add User", command=self.add_user)
        self.add_btn.pack(fill=tk.X, pady=2)
        
        self.update_btn = ttk.Button(btn_frame, text="Update User", command=self.update_user, state=tk.DISABLED)
        self.update_btn.pack(fill=tk.X, pady=2)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete User", command=self.delete_user, state=tk.DISABLED)
        self.delete_btn.pack(fill=tk.X, pady=2)
        
        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_form)
        self.clear_btn.pack(fill=tk.X, pady=2)
    
    def refresh_user_list(self):
        """Refresh the user list from the database"""
        # Clear existing items
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # Get users from DAO
        users = self.user_dao.get_all_users()
        
        # Insert users into treeview
        for user in users:
            self.user_tree.insert('', tk.END, values=(user.id, user.username, user.email, user.role))
    
    def on_user_select(self, event):
        """Handle user selection in the treeview"""
        selection = self.user_tree.selection()
        if selection:
            item = self.user_tree.item(selection[0])
            user_id = item['values'][0]
            
            # Get full user details from DAO
            self.current_user = self.user_dao.get_user_by_username(item['values'][1])
            
            if self.current_user:
                self.username_var.set(self.current_user.username)
                self.email_var.set(self.current_user.email)
                self.role_var.set(self.current_user.role)
                self.password_var.set("")  # Don't show password
                
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
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # Get all users and filter
        all_users = self.user_dao.get_all_users()
        filtered_users = [
            user for user in all_users 
            if search_term in user.username.lower() or 
               search_term in user.email.lower() or 
               search_term in user.role.lower()
        ]
        
        # Insert filtered users into treeview
        for user in filtered_users:
            self.user_tree.insert('', tk.END, values=(user.id, user.username, user.email, user.role))
    
    def add_user(self):
        """Add a new user"""
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        role = self.role_var.get()
        password = self.password_var.get()
        
        if not username or not email or not role or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Create user object
        user = User(username=username, password_hash=password, email=email, role=role)
        
        # Try to create user
        if self.user_dao.create_user(user):
            messagebox.showinfo("Success", "User created successfully")
            self.refresh_user_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Username or email already exists")
    
    def update_user(self):
        """Update the selected user"""
        if not self.current_user:
            return
        
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        role = self.role_var.get()
        password = self.password_var.get()
        
        if not username or not email or not role:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        # Update user object
        self.current_user.username = username
        self.current_user.email = email
        self.current_user.role = role
        
        # If password is provided, update it
        if password:
            self.current_user.password_hash = password
        
        # Try to update user
        if self.user_dao.update_user(self.current_user):
            messagebox.showinfo("Success", "User updated successfully")
            self.refresh_user_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update user")
    
    def delete_user(self):
        """Delete the selected user"""
        if not self.current_user:
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {self.current_user.username}?"):
            if self.user_dao.delete_user(self.current_user.id):
                messagebox.showinfo("Success", "User deleted successfully")
                self.refresh_user_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to delete user")
    
    def clear_form(self):
        """Clear the user details form"""
        self.username_var.set("")
        self.email_var.set("")
        self.role_var.set("")
        self.password_var.set("")
        self.current_user = None
        
        # Clear selection in treeview
        self.user_tree.selection_remove(self.user_tree.selection())
        
        # Disable update/delete buttons, enable add button
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.add_btn.config(state=tk.NORMAL)