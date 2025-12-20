"""
Main entry point for the Advanced Computer Programming project
This application handles user authentication, product management, 
customer registration, and borrowing/returning processes.
"""

def main():
    """Application entry point"""
    print("Starting Advanced Computer Programming Project...")
    
    # Initialize database
    from db.db_init import initialize_database
    initialize_database()
    
    # Start the UI
    from ui.login.login_frame import LoginFrame
    import tkinter as tk
    
    root = tk.Tk()
    app = LoginFrame(root)
    root.mainloop()


if __name__ == "__main__":
    main()