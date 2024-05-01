import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()
        print(f'Current mouse position: x={x}, y={y}', end="\r")
        time.sleep(0.1)  # Pause the loop for 0.1 seconds to reduce output frequency
except KeyboardInterrupt:
    print('Program exited by user.')