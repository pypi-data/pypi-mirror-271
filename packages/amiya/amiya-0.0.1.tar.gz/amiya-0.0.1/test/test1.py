# import pyautogui

# active_window_info = pyautogui.getActiveWindow()
# print(f"Current active/focused window: {active_window_info}")

from elevate import elevate; elevate()

import pyautogui
import time


print("starting in 5 secs...")
time.sleep(5)

ct = 0
try:
    while ct < 999999:
        pyautogui.moveTo(1655, 1520)
        pyautogui.click()
        
        pyautogui.moveTo(1931, 1520)
        pyautogui.click()
        
        pyautogui.moveTo(2180, 1520)
        pyautogui.click()
        
        time.sleep(1.1)
        pyautogui.moveTo(2220, 1520)
        pyautogui.click()
        
        time.sleep(10)
        
        # Start
        pyautogui.moveTo(1968, 2021)
        pyautogui.click()
        time.sleep(2)
        
        # Onwards
        pyautogui.moveTo(1092, 2021)
        pyautogui.click()
        
        pyautogui.press("f")
        
        time.sleep(30)
        
        pyautogui.moveTo(1968, 2021)
        pyautogui.click()
        pyautogui.press("esc")
        
        time.sleep(7)
        
        ct += 1
except KeyboardInterrupt:
    print("Program exited.")


# # import schedule
# # import time

# # def my_task():
# #     print("Running my scheduled task!")

# # # Schedule the task to run daily at 10:30 AM
# # schedule.every().day.at("13:51").do(my_task)

# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)

# import os
# import shutil

# def print_centered(text):
#     # Get the size of the terminal
#     terminal_width, terminal_height = shutil.get_terminal_size((80, 20))  # Default size
    
#     # Split the text into lines
#     lines = text.split('\n')
    
#     # Find the maximum width of the text block
#     max_width = max(len(line) for line in lines)
    
#     # Calculate the left padding to center the text
#     left_padding = (terminal_width - max_width) // 2
    
#     # Print each line with the necessary left padding
#     for line in lines:
#         print(' ' * left_padding + line)

# text = r'''
#        _    __  __ _____   __ _       ____ _     ___  
#       / \  |  \/  |_ _\ \ / // \     / ___| |   |_ _| 
#      / _ \ | |\/| || | \ V // _ \   | |   | |    | |  
#     / ___ \| |  | || |  | |/ ___ \  | |___| |___ | |  
#    /_/   \_\_|  |_|___| |_/_/   \_\  \____|_____|___| 
  
# A lightweight cross-platform automation tool for daily tasks!
#               https://github.com/ReZeroE/Amiya
#                         By Kevin L.
# '''

# print_centered(text)


# # import os
# # import platform

# # def clear_terminal():
# #     # Clear terminal based on platform
# #     if platform.system() == 'Windows':
# #         os.system('cls')
# #     else:
# #         os.system('clear')

# # def supports_color():
# #     # Check if terminal supports ANSI coloring
# #     term = os.environ.get('TERM', '')
# #     return term in ('xterm', 'xterm-256color', 'screen', 'screen-256color', 'tmux', 'tmux-256color')

# # def print_colored(text, color='31'):
# #     print(supports_color())
# #     if supports_color():
# #         print(f"\033[{color}m{text}\033[0m")
# #     else:
# #         print(text)

# # def main():
# #     clear_terminal()
# #     text = r'''
# #            _    __  __ _____   __ _       ____ _     ___  
# #           / \  |  \/  |_ _\ \ / // \     / ___| |   |_ _| 
# #          / _ \ | |\/| || | \ V // _ \   | |   | |    | |  
# #         / ___ \| |  | || |  | |/ ___ \  | |___| |___ | |  
# #        /_/   \_\_|  |_|___| |_/_/   \_\  \____|_____|___| 
    
# #     A lightweight cross-platform automation tool for daily tasks!
# #                   https://github.com/ReZeroE/Amiya
# #                             By Kevin L.
# #     '''

# #     print_centered(text)
# #     print_colored("Welcome to the custom terminal. Type 'exit' to quit.")
# #     while True:
# #         command = input("$ ")
# #         if command.lower() == 'exit':
# #             print("Exiting the custom terminal.")
# #             break
# #         else:
# #             execute_command(command)

# # def execute_command(command):
# #     try:
# #         os.system(command)
# #     except Exception as e:
# #         print_colored(f"Error executing command: {e}", '31')


# # import os
# # import sys

# # def supports_color():
# #     """
# #     Returns True if the running system's terminal supports color, and False
# #     otherwise.
# #     """
# #     plat = sys.platform
# #     supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
# #                                                   'ANSICON' in os.environ)
# #     # isatty is not always implemented, #6223.
# #     is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
# #     return supported_platform and is_a_tty

# # # # Example usage
# # # if supports_color():
# # #     print("ANSI color is supported on this Windows terminal.")
# # # else:
# # #     print("ANSI color is not supported on this Windows terminal.")

# # import os
# # os.system("")  # enables ansi escape characters in terminal

# # COLOR = {
# #     "HEADER": "\033[95m",
# #     "BLUE": "\033[94m",
# #     "GREEN": "\033[92m",
# #     "RED": "\033[91m",
# #     "ENDC": "\033[0m",
# # }

# # from termcolor import colored

# # print(COLOR["GREEN"], "Testing Green!!", COLOR["ENDC"])
# # print(colored("text", "green"))

# # if __name__ == "__main__":
# #     print(supports_color())





# # am.create_app("Chrome", "C:\Program Files\Google\Chrome\Application\chrome.exe")
# # am.create_app("Final Fantasy XIV", "abc/abc.exe")
# # am.create_app("LD Player", "E:\LDPlayer\LDPlayer9\dnplayer.exe")
# # am.print_apps()
# am.add_tag()a
# am.remove_tag()


# am.list_sequences()

# ac = AutomationController("D:/Workspace/Amiya/src/amiya/apps/chrome/automation")
# ac.record_new_sequence("test_auto.json", overwrite=True)
# sequence = ac.load_sequence("test_auto.json")
# sequence.run()
import psutil
for proc in psutil.process_iter(['pid', 'name', 'exe']):
    print(proc.started)