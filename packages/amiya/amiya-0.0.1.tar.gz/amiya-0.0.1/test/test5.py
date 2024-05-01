import sys
import ctypes
import os, time

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

if not is_admin():
    print("Script is not running as admin.")
    # Trying to gain admin privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    print("Script is running as admin.")
    time.sleep(10)
    # Your code that requires admin rights here