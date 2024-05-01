import tkinter as tk
import threading
import time
import sys

def recording():
    global window_event
    window_event = threading.Event()
    duration = 10  # Set the total duration of the recording in seconds

    # Start the recording indicator window in a separate thread
    threading.Thread(target=create_indicator_window, args=(duration,), daemon=True).start()

    try:
        print("Recording started...")
        for remaining in range(duration, 0, -1):
            time.sleep(1)  # Pause for a second
            if window_event.is_set():  # Check if the stop event has been triggered
                print("Recording stopped by user.")
                break
            print(f"{remaining} seconds remaining...")
        else:
            print("Recording finished.")
    finally:
        window_event.set()

def stop_recording():
    global window_event
    window_event.set()  # Set the event to stop the recording

def create_indicator_window(duration):
    LENGTH = 200
    WIDTH = 300
    
    root = tk.Tk()
    root.title("Recording...")
    root.geometry(f"{WIDTH}x{LENGTH}+800+400")
    root.overrideredirect(True)  # Remove window decorations

    # Set the overall background color to black and then make it transparent
    background_color = 'black'
    root.configure(bg=background_color)
    root.attributes('-transparentcolor', background_color)

    canvas = tk.Canvas(root, bg=background_color, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Replace 'black' with the color of your choice for the rounded rectangle
    canvas_color = '#333333'
    radius = 10
    canvas.create_polygon(
        [
            radius,         0,              WIDTH - radius,   0, 
            WIDTH,            radius,         WIDTH,            LENGTH - radius, 
            WIDTH - radius,   LENGTH,            radius,         LENGTH, 
            0,              LENGTH - radius,   0,              radius
        ],
        smooth=True, fill=canvas_color)

    label = tk.Label(canvas, text="Recording...", font=('Helvetica', 16), fg='#FFFFFF', bg=canvas_color)
    label.place(relx=0.5, rely=0.3, anchor='center')

    stop_button = tk.Button(canvas, text='Stop Recording', command=stop_recording, bg='#14628c', fg='#FFFFFF')
    stop_button.place(relx=0.5, rely=0.8, anchor='center', width=200)

    stop_button_2 = tk.Button(canvas, text='Terminate Recording', command=stop_recording, bg='#14628c', fg='#FFFFFF')
    stop_button_2.place(relx=0.5, rely=0.95, anchor='center', width=200)

    # Mouse movement handling
    def on_press(event):
        root._drag_start_x = event.x
        root._drag_start_y = event.y

    def on_drag(event):
        dx = event.x - root._drag_start_x
        dy = event.y - root._drag_start_y
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.geometry(f"+{x}+{y}")

    root.bind('<Button-1>', on_press)
    root.bind('<B1-Motion>', on_drag)

    def update_label(remaining):
        if remaining > 0 and not window_event.is_set():
            label.config(text=f"{remaining} seconds remaining...")
            root.after(1000, update_label, remaining - 1)
        else:
            root.destroy()

    root.after(1000, update_label, duration)
    root.mainloop()

if __name__ == "__main__":
    recording()
