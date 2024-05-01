def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def print_color_text(text, hex_color):
    rgb = hex_to_rgb(hex_color)
    # ANSI escape code for 24-bit (true color): \x1b[38;2;<r>;<g>;<b>m
    escape_seq = f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    print(f"{escape_seq}{text}\x1b[0m")  # Reset to default after

import os
# Usage
os.system("")
print_color_text("This is a text with a custom color!", "#d7ffd4")  # Deep purple color

print("\u2713")  # Prints the checkmark symbol ✓


while True:
    u = input(" > ").strip()
    print_color_text("Hello world! This is a sentence!", u)
    
    
    
    '''
    
    #d7ffd4
    
    
    '''