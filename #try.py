import cv2
import time
import threading
import tkinter as tk
from gaze_tracking import GazeTracking
import word_library
 
class EyeTrackingInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Tracking Interface")
        self.buttons = []
 
        # Create three buttons and add them to the Tkinter window
        for i in range(3):
            button = tk.Button(root, text=f"Button {i+1}", width=20, height=5)
            button.grid(row=i, column=0, padx=20, pady=20)
            self.buttons.append(button)
 
        self.current_index = 0
        self.highlight_button(self.current_index)
        self.selection_start_time = None
        self.selection_threshold = 2  # 2 seconds threshold for selection
 
    def highlight_button(self, index):
        # Highlight the button at the specified index
        for i, button in enumerate(self.buttons):
            if i == index:
                button.config(bg="yellow")
            else:
                button.config(bg="SystemButtonFace")
 
    def select_button(self):
        # Select the currently highlighted button
        button = self.buttons[self.current_index]
        print(f"Selected {button.cget('text')}")
 
    def move_selection(self, direction):
        # Move the selection up or down based on the gaze direction
        if direction == "up" and self.current_index > 0:
            self.current_index -= 1
        elif direction == "down" and self.current_index < len(self.buttons) - 1:
            self.current_index += 1
        self.highlight_button(self.current_index)
        self.selection_start_time = time.time()  # Reset the selection timer
 
    def check_selection(self):
        # Check if the gaze has stayed on the current selection for the threshold duration
        if self.selection_start_time and (time.time() - self.selection_start_time > self.selection_threshold):
            self.select_button()
            self.selection_start_time = None  # Reset the selection timer
 
class EyeTrackingController:
    def __init__(self, interface):
        self.interface = interface
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        self.direction_start_time = None
        self.current_direction = None
        self.direction_threshold = 0.5  # 0.5 seconds threshold for direction detection
        self.last_selection_check_time = time.time()
 
    def check_gaze_direction(self):
        # Determine the gaze direction
        if self.gaze.is_right():
            return "right"
        elif self.gaze.is_left():
            return "left"
        elif self.gaze.is_up():
            return "up"
        elif self.gaze.is_down():
            return "down"
        else:
            return "center"
 
    def run(self):
        while True:
            # Get a new frame from the webcam
            _, frame = self.webcam.read()
            # Analyze the frame using GazeTracking
            self.gaze.refresh(frame)
            detected_direction = self.check_gaze_direction()
 
            if detected_direction != self.current_direction:
                self.current_direction = detected_direction
                self.direction_start_time = time.time()
            else:
                if time.time() - self.direction_start_time > self.direction_threshold:
                    # Move the selection if the gaze has stayed in the same direction for the threshold duration
                    if self.current_direction in ["up", "down"]:
                        self.interface.move_selection(self.current_direction)
                    self.current_direction = None  # Reset direction after moving
 
            # Check selection if enough time has passed since the last check
            if time.time() - self.last_selection_check_time > 0.1:
                self.interface.check_selection()
                self.last_selection_check_time = time.time()
 
            # Display the frame with annotations
            frame = self.gaze.annotated_frame()
            cv2.imshow("Demo", frame)
            if cv2.waitKey(1) == 27:  # Exit on pressing 'ESC'
                break
 
        self.webcam.release()
        cv2.destroyAllWindows()
 
def run_interface():
    root = word_library
    app = EyeTrackingInterface(root)
    root.mainloop()
 
def run_eye_tracking(interface):
    controller = EyeTrackingController(interface)
    controller.run()
 
if __name__ == "__main__":
    # Run the interface in a separate thread
    interface_thread = threading.Thread(target=run_interface)
    interface_thread.start()
 
    # Allow the interface to initialize
    time.sleep(1)
 
    # Find the interface instance and run eye tracking
    for thread in threading.enumerate():
        if hasattr(thread, '_target') and thread._target == run_interface:
            root = thread._target.__globals__['root']
            interface_instance = EyeTrackingInterface(root)
 
    # Run the eye tracking controller with the interface instance
    run_eye_tracking(interface_instance)