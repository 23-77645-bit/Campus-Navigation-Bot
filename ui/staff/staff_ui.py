"""
Staff UI Main Interface
Main window for staff users with navigation to different panels
"""
import tkinter as tk
from tkinter import ttk
from service.session_manager import SessionManager
from ui.staff.customer_registration_panel import CustomerRegistrationPanel
from ui.staff.borrowing_history_panel import BorrowingHistoryPanel
from ui.staff.return_panel import ReturnPanel
from ui.staff.purchase_panel import PurchasePanel


class StaffUI:
    def __init__(self, parent):
        self.parent = parent
        self.session_manager = SessionManager()
        
        # Check if user is logged in and is staff
        current_user = self.session_manager.get_current_user()
        if not current_user or not current_user.is_staff():
            tk.messagebox.showerror("Access Denied", "Staff access required")
            self.parent.destroy()
            return
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the staff user interface"""
        self.parent.title(f"Staff Dashboard - Welcome {self.session_manager.get_current_user().username}")
        self.parent.geometry("1000x700")
        self.parent.minsize(800, 600)
        
        # Create main frame
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create panels
        self.customer_panel = CustomerRegistrationPanel(self.notebook)
        self.borrowing_panel = BorrowingHistoryPanel(self.notebook)
        self.return_panel = ReturnPanel(self.notebook)
        self.purchase_panel = PurchasePanel(self.notebook)
        
        # Add panels to notebook
        self.notebook.add(self.customer_panel, text="Customers")
        self.notebook.add(self.borrowing_panel, text="Borrowings")
        self.notebook.add(self.return_panel, text="Returns")
        self.notebook.add(self.purchase_panel, text="Purchases")
        
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