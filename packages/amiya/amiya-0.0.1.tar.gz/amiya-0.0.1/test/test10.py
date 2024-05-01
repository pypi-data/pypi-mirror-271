import subprocess

from ctypes import windll
windll.user32.SetProcessDPIAware()

    
pid = None
while True:
    result = subprocess.run(["./get_window_size.exe", "25592"], capture_output=True, text=True)
    if result.returncode == 0:
        size = result.stdout.strip()
        print(f"{size}")
        break