def calculate_new_coordinate(prev_monitor_size, prev_window_size, prev_coord,
                             current_monitor_size, current_window_size):
    """
    Calculate the new screen coordinates considering changes in monitor size,
    and assuming the window is centered on the screen.

    Parameters:
    - prev_monitor_size: Tuple (width, height) of the previous monitor size
    - prev_window_size: Tuple (width, height) of the previous window size
    - prev_coord: Tuple (x, y) of the previous coordinates within the window
    - current_monitor_size: Tuple (width, height) of the current monitor size
    - current_window_size: Tuple (width, height) of the current window size
    
    Returns:
    - Tuple (new_x, new_y) representing the new coordinates within the screen
    """

    # Calculate the center of both monitors
    prev_center_x = prev_monitor_size[0] / 2
    prev_center_y = prev_monitor_size[1] / 2
    current_center_x = current_monitor_size[0] / 2
    current_center_y = current_monitor_size[1] / 2

    # Calculate the top-left corner of the centered window on each monitor
    prev_window_origin_x = prev_center_x - (prev_window_size[0] / 2)
    prev_window_origin_y = prev_center_y - (prev_window_size[1] / 2)
    current_window_origin_x = current_center_x - (current_window_size[0] / 2)
    current_window_origin_y = current_center_y - (current_window_size[1] / 2)

    # Calculate the absolute position of the previous coordinate on the monitor
    prev_absolute_x = prev_window_origin_x + prev_coord[0]
    prev_absolute_y = prev_window_origin_y + prev_coord[1]

    # Calculate the relative position of the previous coordinate within the previous monitor
    rel_x = (prev_absolute_x - prev_window_origin_x) / prev_window_size[0]
    rel_y = (prev_absolute_y - prev_window_origin_y) / prev_window_size[1]

    # Apply the relative position to the current window dimensions
    new_x = current_window_origin_x + (rel_x * current_window_size[0])
    new_y = current_window_origin_y + (rel_y * current_window_size[1])

    return (new_x, new_y)

# Example usage
prev_monitor_size = (1920, 1080)
prev_window_size = (800, 600)
prev_coord = (400, 300)  # Center of the previous window

current_monitor_size = (2560, 1440)
current_window_size = (800, 600)  # Same window size, different monitor size

new_coord = calculate_new_coordinate(prev_monitor_size, prev_window_size, prev_coord,
                                     current_monitor_size, current_window_size)
print(f"New coordinate: {new_coord}")