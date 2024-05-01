import subprocess



    
pid = None
while True:
    result = subprocess.run(["./get_active_pid.exe"], capture_output=True, text=True)
    if result.returncode == 0:
        pid = result.stdout.strip()
        print(f"     {pid}               ", end="\r")