#!/usr/bin/env python3
"""
HUNGER Restaurant Billing System - GUI Installer
Simple GUI installer with progress tracking
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import subprocess
import threading
from pathlib import Path
import shutil

class HUNGERInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HUNGER Restaurant Billing System - Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
        # Variables
        self.install_path = tk.StringVar(value=r"C:\Program Files\HUNGER Restaurant Billing System")
        self.install_progress = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to install")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="HUNGER Restaurant Billing System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Professional Desktop Billing System", 
                                  font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Features frame
        features_frame = ttk.LabelFrame(main_frame, text="Features", padding="10")
        features_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        features_text = """• Complete Restaurant Billing System
• GST Calculation and Compliance
• UPI QR Code Generation
• User Management with Role-Based Access
• Sales Reports and Analytics
• Automatic Update Notifications
• SQLite Database (Built-in)"""
        
        ttk.Label(features_frame, text=features_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Installation path
        path_frame = ttk.LabelFrame(main_frame, text="Installation Location", padding="10")
        path_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Entry(path_frame, textvariable=self.install_path, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(path_frame, text="Browse", command=self.browse_path).grid(row=0, column=1, padx=(10, 0))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Installation Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.install_progress, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_text)
        self.status_label.grid(row=1, column=0, columnspan=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        self.install_button = ttk.Button(button_frame, text="Install", command=self.start_installation)
        self.install_button.grid(row=0, column=0, padx=(0, 10))
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.root.quit)
        self.cancel_button.grid(row=0, column=1)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def browse_path(self):
        """Browse for installation path"""
        path = filedialog.askdirectory(title="Select Installation Directory")
        if path:
            self.install_path.set(os.path.join(path, "HUNGER Restaurant Billing System"))
            
    def start_installation(self):
        """Start the installation process"""
        self.install_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        
        # Start installation in a separate thread
        thread = threading.Thread(target=self.install_application)
        thread.daemon = True
        thread.start()
        
    def install_application(self):
        """Install the application"""
        try:
            install_dir = Path(self.install_path.get())
            
            # Step 1: Create installation directory
            self.update_status("Creating installation directory...")
            self.update_progress(10)
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # Step 2: Copy application files
            self.update_status("Copying application files...")
            self.update_progress(20)
            
            # Copy restaurant_billing module
            if Path("restaurant_billing").exists():
                shutil.copytree("restaurant_billing", install_dir / "restaurant_billing", dirs_exist_ok=True)
            
            # Copy main files
            files_to_copy = ["main.py", "requirements.txt", "README.md", "LICENSE.txt"]
            for file in files_to_copy:
                if Path(file).exists():
                    shutil.copy2(file, install_dir / file)
            
            # Step 3: Check Python installation
            self.update_status("Checking Python installation...")
            self.update_progress(30)
            
            try:
                result = subprocess.run([sys.executable, "--version"], 
                                      capture_output=True, text=True, check=True)
                python_version = result.stdout.strip()
                print(f"Python found: {python_version}")
            except subprocess.CalledProcessError:
                self.update_status("Python not found! Please install Python 3.11+")
                self.show_error("Python 3.11+ is required but not found.\nPlease install Python from https://python.org")
                return
            
            # Step 4: Install Python dependencies
            self.update_status("Installing Python dependencies...")
            self.update_progress(50)
            
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                             check=True, capture_output=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                             cwd=install_dir, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                self.update_status("Failed to install dependencies")
                self.show_error(f"Failed to install Python dependencies: {e}")
                return
            
            # Step 5: Initialize database
            self.update_status("Initializing database...")
            self.update_progress(70)
            
            try:
                subprocess.run([sys.executable, "-c", 
                              "from restaurant_billing.db import init_db; init_db(); print('Database initialized')"], 
                             cwd=install_dir, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                self.update_status("Database initialization failed")
                self.show_error(f"Failed to initialize database: {e}")
                return
            
            # Step 6: Create shortcuts
            self.update_status("Creating shortcuts...")
            self.update_progress(85)
            
            self.create_shortcuts(install_dir)
            
            # Step 7: Complete installation
            self.update_status("Installation completed successfully!")
            self.update_progress(100)
            
            # Show success message
            self.root.after(0, self.show_success)
            
        except Exception as e:
            self.update_status(f"Installation failed: {e}")
            self.root.after(0, lambda: self.show_error(f"Installation failed: {e}"))
            
    def create_shortcuts(self, install_dir):
        """Create desktop and start menu shortcuts"""
        try:
            # Create batch file launcher
            batch_path = install_dir / "start_desktop.bat"
            with open(batch_path, 'w') as f:
                f.write('@echo off\n')
                f.write(f'cd /d "{install_dir}"\n')
                f.write('python main.py\n')
                f.write('pause\n')
                
        except Exception as e:
            print(f"Failed to create shortcuts: {e}")
                
    def update_status(self, message):
        """Update status message"""
        self.root.after(0, lambda: self.status_text.set(message))
        print(message)
        
    def update_progress(self, value):
        """Update progress bar"""
        self.root.after(0, lambda: self.install_progress.set(value))
        
    def show_success(self):
        """Show success message"""
        messagebox.showinfo("Installation Complete", 
                           "HUNGER Restaurant Billing System has been installed successfully!\n\n"
                           f"Installation location: {self.install_path.get()}\n\n"
                           "Default login credentials:\n"
                           "Username: owner\n"
                           "Password: 1234\n\n"
                           "Click OK to launch the application.")
        
        # Launch application
        try:
            install_dir = Path(self.install_path.get())
            subprocess.Popen([sys.executable, "main.py"], cwd=install_dir)
        except Exception as e:
            print(f"Failed to launch application: {e}")
            
        self.root.quit()
        
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Installation Error", message)
        self.install_button.config(state="normal")
        self.cancel_button.config(state="normal")
        
    def run(self):
        """Run the installer"""
        self.root.mainloop()

if __name__ == "__main__":
    # Check if running on Windows
    if sys.platform != "win32":
        print("This installer is designed for Windows only.")
        sys.exit(1)
        
    # Check for required modules
    try:
        import tkinter
    except ImportError:
        print("tkinter is required but not installed.")
        sys.exit(1)
        
    installer = HUNGERInstaller()
    installer.run()
