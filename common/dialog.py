"""
Common Dialogs Module
Provides reusable dialog windows for the application
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class Dialog:
    @staticmethod
    def show_info(title: str, message: str, parent=None):
        """Show an information dialog"""
        messagebox.showinfo(title, message, parent=parent)

    @staticmethod
    def show_warning(title: str, message: str, parent=None):
        """Show a warning dialog"""
        messagebox.showwarning(title, message, parent=parent)

    @staticmethod
    def show_error(title: str, message: str, parent=None):
        """Show an error dialog"""
        messagebox.showerror(title, message, parent=parent)

    @staticmethod
    def ask_yes_no(title: str, message: str, parent=None) -> bool:
        """Ask a yes/no question and return the result"""
        return messagebox.askyesno(title, message, parent=parent)

    @staticmethod
    def ask_ok_cancel(title: str, message: str, parent=None) -> bool:
        """Ask an OK/cancel question and return the result"""
        return messagebox.askokcancel(title, message, parent=parent)

    @staticmethod
    def ask_retry_cancel(title: str, message: str, parent=None) -> bool:
        """Ask a retry/cancel question and return the result"""
        return messagebox.askretrycancel(title, message, parent=parent)

    @staticmethod
    def ask_question(title: str, message: str, parent=None) -> bool:
        """Ask a yes/no question and return the result"""
        return messagebox.askquestion(title, message, parent=parent)

    @staticmethod
    def ask_string(title: str, prompt: str, initial_value: str = "", parent=None) -> str:
        """Ask for a string input"""
        return simpledialog.askstring(title, prompt, initialvalue=initial_value, parent=parent)

    @staticmethod
    def ask_integer(title: str, prompt: str, initial_value: int = 0, 
                    min_value: int = None, max_value: int = None, parent=None) -> int:
        """Ask for an integer input"""
        return simpledialog.askinteger(title, prompt, initialvalue=initial_value, 
                                      minvalue=min_value, maxvalue=max_value, parent=parent)

    @staticmethod
    def ask_float(title: str, prompt: str, initial_value: float = 0.0, 
                  min_value: float = None, max_value: float = None, parent=None) -> float:
        """Ask for a float input"""
        return simpledialog.askfloat(title, prompt, initialvalue=initial_value, 
                                    minvalue=min_value, maxvalue=max_value, parent=parent)

    @staticmethod
    def show_progress_dialog(title: str, message: str, parent=None) -> tk.Toplevel:
        """Show a progress dialog (returns the dialog window for manual control)"""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("300x100")
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(parent)
        dialog.grab_set()
        
        # Add message label
        label = tk.Label(dialog, text=message)
        label.pack(pady=10)
        
        # Add progress bar
        progress = ttk.Progressbar(dialog, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill=tk.X)
        progress.start()
        
        return dialog

    @staticmethod
    def show_custom_confirmation_dialog(title: str, message: str, 
                                      positive_text: str = "Yes", 
                                      negative_text: str = "No", 
                                      parent=None) -> bool:
        """Show a custom confirmation dialog with custom button texts"""
        result = tk.BooleanVar()
        
        def on_positive():
            result.set(True)
            dialog.destroy()
        
        def on_negative():
            result.set(False)
            dialog.destroy()
        
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("300x120")
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(parent)
        dialog.grab_set()
        
        # Add message label
        label = tk.Label(dialog, text=message)
        label.pack(pady=15)
        
        # Add buttons frame
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        # Add buttons
        positive_btn = tk.Button(button_frame, text=positive_text, command=on_positive)
        positive_btn.pack(side=tk.LEFT, padx=5)
        
        negative_btn = tk.Button(button_frame, text=negative_text, command=on_negative)
        negative_btn.pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result.get()