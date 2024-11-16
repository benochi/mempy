import psutil
#only use this if process name needs tracked down.
def find_process_by_name(process_name):
    """Find and print all processes matching a name."""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                print(f"Found process: {proc.info['name']} (PID: {proc.info['pid']})")
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"Process '{process_name}' not found.")
    return None

if __name__ == "__main__":
    process_name = "Drill Core"  # Replace with the app name you're looking for
    pid = find_process_by_name(process_name)
    if pid:
        print(f"Attach to PID {pid}.")
