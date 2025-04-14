from monitor.system_monitor import ResourceMonitor

if __name__ == "__main__":
    monitor = ResourceMonitor()
    monitor.root.protocol("WM_DELETE_WINDOW", monitor.cleanup)
    monitor.root.mainloop()
