"""
Admin UI Main Interface
Main window for admin users with navigation to different panels
"""
import tkinter as tk
from tkinter import ttk
from service.session_manager import SessionManager
from ui.admin.user_management_panel import UserManagementPanel
from ui.admin.product_crud_panel import ProductCRUDPanel
from ui.admin.customer_panel import CustomerPanel
from ui.admin.borrowing_report_panel import BorrowingReportPanel
from ui.admin.audit_log_panel import AuditLogPanel


class AdminUI:
    def __init__(self, parent):
        self.parent = parent
        self.session_manager = SessionManager()
        
        # Check if user is logged in and is admin
        current_user = self.session_manager.get_current_user()
        if not current_user or not current_user.is_admin():
            tk.messagebox.showerror("Access Denied", "Admin access required")
            self.parent.destroy()
            return
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the admin user interface"""
        self.parent.title(f"Admin Dashboard - Welcome {self.session_manager.get_current_user().username}")
        self.parent.geometry("1000x700")
        self.parent.minsize(800, 600)
        
        # Create main frame
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create panels
        self.user_panel = UserManagementPanel(self.notebook)
        self.product_panel = ProductCRUDPanel(self.notebook)
        self.customer_panel = CustomerPanel(self.notebook)
        self.borrowing_panel = BorrowingReportPanel(self.notebook)
        self.audit_panel = AuditLogPanel(self.notebook)
        
        # Add panels to notebook
        self.notebook.add(self.user_panel, text="Users")
        self.notebook.add(self.product_panel, text="Products")
        self.notebook.add(self.customer_panel, text="Customers")
        self.notebook.add(self.borrowing_panel, text="Borrowings")
        self.notebook.add(self.audit_panel, text="Audit Logs")
        
        # Add logout button
        logout_btn = ttk.Button(main_frame, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.BOTTOM, pady=5)
        
    def logout(self):
        """Handle user logout"""
        from service.session_manager import SessionManager
        session = SessionManager()
        session.logout()
        
        # Close current window and open login
        self.parent.destroy()
        
        # Import here to avoid circular imports
        from ui.login.login_frame import LoginFrame
        login_root = tk.Tk()
        login_app = LoginFrame(login_root)
        login_root.mainloop()