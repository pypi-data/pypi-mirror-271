import win32con
import win32gui
import win32process
import win32api
from ctypes import windll
import pygetwindow as gw
user32 = windll.user32
user32.SetProcessDPIAware() # optional, makes functions return real pixel numbers instead of scaled values

full_screen_rect = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

def get_window_info_by_pid(pid):
    # Attempt to find the window using the PID
    windows = gw.getWindowsWithTitle('')  # Get all windows
    for window in windows:
        # Fetch the process ID associated with the window handle
        _, window_pid = win32process.GetWindowThreadProcessId(window._hWnd)
        if window_pid == pid:
            # Return details if PID matches
            return {
                'left': window.left,
                'top': window.top,
                'width': window.width,
                'height': window.height,
                'is_fullscreen': window.isMaximized
            }
    return "No window found with that PID"


while True:
    
    import time
    t = time.time()
    
    # Example usage
    pid = 25592  # Replace this with the actual PID you want to check
    info = get_window_info_by_pid(pid)
    print(info)

    print(time.time() - t)
    exit()



def isRealWindow(hWnd):
    '''Return True iff given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW) != 0 and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def getWindowDetailsByPid(pid) -> list[dict]:
    '''
    Return a list of tuples (handler, (left, top, width, height, is_maximized)) for each real window belonging to a specific PID.
    '''
    def callback(hWnd, windows: list):
        try:
            window_pid = win32process.GetWindowThreadProcessId(hWnd)[1]
            if window_pid == pid:
                rect = win32gui.GetWindowRect(hWnd)
                
                window_info = {
                    "top": rect[1],
                    "left": rect[0],
                    "width": rect[2] - rect[0],
                    "height": rect[3] - rect[1]
                }
                windows.append(window_info)
                
        except win32api.error as e:
            print(f"Failed to get process for hWnd {hWnd}: {e}")

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

# Usage example: Assuming you have a PID to query
pid = 4828  # Replace this with the actual PID you want to check
# 34464
# 4828
import time
t = time.time()


while True:
    window_details = getWindowDetailsByPid(pid)
    for detail in window_details:
        print(f"   {detail}                ")
    exit()

print(time.time() - t)