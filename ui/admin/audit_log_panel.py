"""
Audit Log Panel
Displays system audit logs for admin review
"""
import tkinter as tk
from tkinter import ttk
from service.admin_activity_logger import AdminActivityLogger


class AuditLogPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.logger = AdminActivityLogger()
        
        self.setup_ui()
        self.refresh_audit_logs()
        
    def setup_ui(self):
        """Setup the audit log interface"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(controls_frame, text="Refresh Logs", command=self.refresh_audit_logs)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Label for limit
        ttk.Label(controls_frame, text="Show last:").pack(side=tk.LEFT, padx=(10, 5))
        
        # Limit entry
        self.limit_var = tk.StringVar(value="100")
        limit_entry = ttk.Entry(controls_frame, textvariable=self.limit_var, width=10)
        limit_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Label for logs
        ttk.Label(controls_frame, text="logs").pack(side=tk.LEFT)
        
        # Log list
        columns = ('Timestamp', 'User', 'Action', 'Table', 'Record ID', 'Old Values', 'New Values')
        self.log_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        for col in columns:
            self.log_tree.heading(col, text=col)
            if col == 'Old Values' or col == 'New Values':
                self.log_tree.column(col, width=150)
            else:
                self.log_tree.column(col, width=100)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.log_tree.yview)
        self.log_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.log_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def refresh_audit_logs(self):
        """Refresh the audit log list from the database"""
        try:
            limit = int(self.limit_var.get())
            if limit <= 0:
                limit = 100
        except ValueError:
            limit = 100
        
        # Clear existing items
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        
        # Get audit logs from logger
        logs = self.logger.get_audit_logs(limit)
        
        # Insert logs into treeview
        for log in logs:
            self.log_tree.insert('', tk.END, values=(
                log['timestamp'], 
                log['username'], 
                log['action'], 
                log['table_affected'], 
                log['record_id'], 
                log['old_values'], 
                log['new_values']
            ))