import psutil

process = psutil.Process(4828)
# Terminate child processes
print(process.parent())

for child in process.children(recursive=True):
    print(child.name())
    
    
    
# import psutil

# def find_and_kill_processes_by_path(executable_path):
#     # Normalize the executable path for accurate comparison
#     normalized_path = os.path.realpath(executable_path)

#     # Iterate over all running processes
#     for proc in psutil.process_iter(['pid', 'exe', 'children']):
#         try:
#             # Check if process executable matches the provided path
#             if proc.info['exe'] and os.path.realpath(proc.info['exe']) == normalized_path:
#                 # Kill the process and its children
#                 process = psutil.Process(proc.info['pid'])
#                 # Terminate child processes
#                 for child in process.children(recursive=True):
#                     child.terminate()
#                 # Terminate the main process
#                 process.terminate()
#                 print(f"Terminated {proc.info['exe']} (PID: {proc.info['pid']}) and its children.")
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass  # Ignore processes that no longer exist or access is denied

# if __name__ == "__main__":
#     import os
#     path_to_executable = input("Enter the path to the executable: ")
#     find_and_kill_processes_by_path(path_to_executable)
