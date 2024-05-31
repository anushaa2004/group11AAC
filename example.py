"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
from pynput.mouse import Controller 
import word_library 


gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
mouse = Controller()

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
        mouse.position = (720,900)
    elif gaze.is_right():
        text = "Looking right"
        mouse.position = (1440,450)
    elif gaze.is_left():
        text = "Looking left"
        mouse.position = (0,450)
    elif gaze.is_center():
        text = "Looking center"
        mouse.position = (720,450)
    elif gaze.is_up():
        text = "Looking up"
        mouse.position = (720,0)
    elif gaze.is_down():
        text = "Looking down"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    vertical_ratio = gaze.vertical_ratio()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "vertical ratio: "+ str(vertical_ratio), (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.imshow("Demo", frame)
   
webcam.release()
cv2.destroyAllWindows()
