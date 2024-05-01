import shutil
from termcolor import colored

def print_centered(text):
    terminal_width, terminal_height = shutil.get_terminal_size((80, 20))  # Default size
    
    lines = text.split('\n')
    max_width = max(len(line) for line in lines)
    left_padding = (terminal_width - max_width) // 2
    
    for line in lines:
        print(' ' * left_padding + line)
        

c = colored('''
       _    __  __ _____   __ _       ____ _     ___  
      / \  |  \/  |_ _\ \ / // \     / ___| |   |_ _| 
     / _ \ | |\/| || | \ V // _ \   | |   | |    | |  
    / ___ \| |  | || |  | |/ ___ \  | |___| |___ | |  
   /_/   \_\_|  |_|___| |_/_/   \_\  \____|_____|___|
''', "cyan")

l = colored('''
A lightweight cross-platform automation tool for daily tasks!
              https://github.com/ReZeroE/Amiya
                        By Kevin L.   
''', "light_blue")

print_centered(
f'''
{c}{l}
''')