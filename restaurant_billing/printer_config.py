"""
Printer Configuration Utility
Helps configure printer settings for full-width printing
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .config import CONFIG
from .printing_fixed import test_printer_width, configure_printer_for_full_width


class PrinterConfigDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Printer Configuration")
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Printer Configuration", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Printer Type Selection
        type_frame = ttk.LabelFrame(main_frame, text="Printer Type", padding="10")
        type_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.printer_type = tk.StringVar(value=CONFIG.printer_type)
        
        ttk.Radiobutton(type_frame, text="OS Default Printer", 
                       variable=self.printer_type, value="os").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(type_frame, text="ESC/POS USB Printer", 
                       variable=self.printer_type, value="escpos_usb").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(type_frame, text="ESC/POS Network Printer", 
                       variable=self.printer_type, value="escpos_network").grid(row=2, column=0, sticky=tk.W)
        
        # Paper Width Configuration
        width_frame = ttk.LabelFrame(main_frame, text="Paper Width", padding="10")
        width_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(width_frame, text="Characters per line:").grid(row=0, column=0, sticky=tk.W)
        self.paper_width = tk.IntVar(value=CONFIG.paper_width_chars)
        width_spinbox = ttk.Spinbox(width_frame, from_=32, to=120, width=10, 
                                   textvariable=self.paper_width)
        width_spinbox.grid(row=0, column=1, padx=(10, 0))
        
        # Width recommendations
        recommendations = ttk.Label(width_frame, 
                                   text="Recommendations:\n• 32 chars: 58mm thermal printer\n• 42 chars: 80mm thermal printer\n• 80 chars: Full page width")
        recommendations.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # ESC/POS Settings (hidden by default)
        self.escpos_frame = ttk.LabelFrame(main_frame, text="ESC/POS Settings", padding="10")
        self.escpos_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # USB Settings
        usb_frame = ttk.Frame(self.escpos_frame)
        usb_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(usb_frame, text="USB Vendor ID:").grid(row=0, column=0, sticky=tk.W)
        self.usb_vendor = tk.StringVar(value=str(CONFIG.escpos_vendor_id or ""))
        ttk.Entry(usb_frame, textvariable=self.usb_vendor, width=15).grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(usb_frame, text="USB Product ID:").grid(row=0, column=2, padx=(20, 0))
        self.usb_product = tk.StringVar(value=str(CONFIG.escpos_product_id or ""))
        ttk.Entry(usb_frame, textvariable=self.usb_product, width=15).grid(row=0, column=3, padx=(10, 0))
        
        # Network Settings
        network_frame = ttk.Frame(self.escpos_frame)
        network_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(network_frame, text="Host:").grid(row=0, column=0, sticky=tk.W)
        self.network_host = tk.StringVar(value=CONFIG.escpos_host or "")
        ttk.Entry(network_frame, textvariable=self.network_host, width=20).grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(network_frame, text="Port:").grid(row=0, column=2, padx=(20, 0))
        self.network_port = tk.StringVar(value=str(CONFIG.escpos_port))
        ttk.Entry(network_frame, textvariable=self.network_port, width=10).grid(row=0, column=3, padx=(10, 0))
        
        # Test Printer Button
        test_frame = ttk.Frame(main_frame)
        test_frame.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Button(test_frame, text="Test Printer Width", 
                  command=self.test_printer).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(test_frame, text="Configure Full-Width", 
                  command=self.configure_full_width).grid(row=0, column=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Save", command=self.save_config).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=1)
        
        # Show/hide ESC/POS settings based on printer type
        self.printer_type.trace('w', self.on_printer_type_change)
        self.on_printer_type_change()
        
    def on_printer_type_change(self, *args):
        """Show/hide ESC/POS settings based on printer type"""
        if self.printer_type.get() in ["escpos_usb", "escpos_network"]:
            self.escpos_frame.grid()
        else:
            self.escpos_frame.grid_remove()
            
    def test_printer(self):
        """Test printer width"""
        try:
            configure_printer_for_full_width()
            test_printer_width()
            messagebox.showinfo("Test", "Printer width test completed. Check console output.")
        except Exception as e:
            messagebox.showerror("Test Failed", f"Printer test failed: {e}")
            
    def configure_full_width(self):
        """Configure printer for full-width printing"""
        try:
            configure_printer_for_full_width()
            messagebox.showinfo("Configuration", "Printer configured for full-width printing!")
        except Exception as e:
            messagebox.showerror("Configuration Failed", f"Configuration failed: {e}")
            
    def save_config(self):
        """Save printer configuration"""
        try:
            # Update CONFIG with new values
            global CONFIG
            CONFIG.printer_type = self.printer_type.get()
            CONFIG.paper_width_chars = self.paper_width.get()
            
            if self.printer_type.get() == "escpos_usb":
                CONFIG.escpos_vendor_id = int(self.usb_vendor.get()) if self.usb_vendor.get() else None
                CONFIG.escpos_product_id = int(self.usb_product.get()) if self.usb_product.get() else None
            elif self.printer_type.get() == "escpos_network":
                CONFIG.escpos_host = self.network_host.get() if self.network_host.get() else None
                CONFIG.escpos_port = int(self.network_port.get()) if self.network_port.get() else 9100
            
            messagebox.showinfo("Configuration Saved", "Printer configuration saved successfully!")
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Save Failed", f"Failed to save configuration: {e}")


def open_printer_config(parent):
    """Open printer configuration dialog"""
    PrinterConfigDialog(parent)
