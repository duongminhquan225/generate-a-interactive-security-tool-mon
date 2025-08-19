# 1yqi_generate_a_inte.py

import tkinter as tk
from tkinter import ttk
import datetime
import threading
import socket
import psutil
import os

# Configuration
monitor_name = "Security Tool Monitor"
window_width = 800
window_height = 600

# Network Monitoring Configuration
network_interfaces = ["eth0", "wlan0"]

# Process Monitoring Configuration
monitored_processes = ["chrome.exe", "firefox.exe"]

# System Monitoring Configuration
cpu_threshold = 80
memory_threshold = 80
disk_threshold = 80

class SecurityToolMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title(monitor_name)
        self.root.geometry(f"{window_width}x{window_height}")

        # Create tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        # Create frames
        self.network_frame = ttk.Frame(self.tabs)
        self.process_frame = ttk.Frame(self.tabs)
        self.system_frame = ttk.Frame(self.tabs)

        # Add frames to tabs
        self.tabs.add(self.network_frame, text="Network")
        self.tabs.add(self.process_frame, text="Processes")
        self.tabs.add(self.system_frame, text="System")

        # Network Monitoring
        self.network_label = ttk.Label(self.network_frame, text="Network Interface Status:")
        self.network_label.pack(fill="x", pady=10)

        self.network_interfaces_status = {}
        for interface in network_interfaces:
            self.network_interfaces_status[interface] = ttk.Label(self.network_frame, text=f"{interface}: Offline")
            self.network_interfaces_status[interface].pack(fill="x")

        # Process Monitoring
        self.process_label = ttk.Label(self.process_frame, text="Process Status:")
        self.process_label.pack(fill="x", pady=10)

        self.process_status = {}
        for process in monitored_processes:
            self.process_status[process] = ttk.Label(self.process_frame, text=f"{process}: Not Running")
            self.process_status[process].pack(fill="x")

        # System Monitoring
        self.system_label = ttk.Label(self.system_frame, text="System Status:")
        self.system_label.pack(fill="x", pady=10)

        self.cpu_label = ttk.Label(self.system_frame, text="CPU Utilization: 0%")
        self.cpu_label.pack(fill="x")

        self.memory_label = ttk.Label(self.system_frame, text="Memory Utilization: 0%")
        self.memory_label.pack(fill="x")

        self.disk_label = ttk.Label(self.system_frame, text="Disk Utilization: 0%")
        self.disk_label.pack(fill="x")

        # Start monitoring
        self.monitor_thread = threading.Thread(target=self.monitor_system)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def monitor_system(self):
        while True:
            # Network Monitoring
            for interface in network_interfaces:
                if self.is_interface_up(interface):
                    self.network_interfaces_status[interface].config(text=f"{interface}: Online")
                else:
                    self.network_interfaces_status[interface].config(text=f"{interface}: Offline")

            # Process Monitoring
            for process in monitored_processes:
                if self.is_process_running(process):
                    self.process_status[process].config(text=f"{process}: Running")
                else:
                    self.process_status[process].config(text=f"{process}: Not Running")

            # System Monitoring
            cpu_utilization = psutil.cpu_percent(interval=1)
            if cpu_utilization > cpu_threshold:
                self.cpu_label.config(text=f"CPU Utilization: {cpu_utilization}% - HIGH")
            else:
                self.cpu_label.config(text=f"CPU Utilization: {cpu_utilization}%")

            memory_utilization = psutil.virtual_memory().percent
            if memory_utilization > memory_threshold:
                self.memory_label.config(text=f"Memory Utilization: {memory_utilization}% - HIGH")
            else:
                self.memory_label.config(text=f"Memory Utilization: {memory_utilization}%")

            disk_utilization = psutil.disk_usage('/').percent
            if disk_utilization > disk_threshold:
                self.disk_label.config(text=f"Disk Utilization: {disk_utilization}% - HIGH")
            else:
                self.disk_label.config(text=f"Disk Utilization: {disk_utilization}%")

            # Update GUI
            self.root.update_idletasks()

    def is_interface_up(self, interface):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((interface, 0))
            return True
        except socket.error:
            return False

    def is_process_running(self, process):
        for p in psutil.process_iter():
            if p.name().lower() == process.lower():
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityToolMonitor(root)
    root.mainloop()