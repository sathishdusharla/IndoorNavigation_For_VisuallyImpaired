import cv2
import threading
import numpy as np
import logging
from modules import obstacle_detection as od, navigation_guidance as nav
import voice_commands as vc

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

stop_event = threading.Event()
navigation_active = False  # Flag to track if navigation is running

def start_navigation(stop_event):
    """Handles AI-powered navigation."""
    global navigation_active
    if navigation_active:
        return
    navigation_active = True

    logging.info("Starting Indoor Navigation System...")
    vc.provide_audio_feedback("Navigation started. Listening for commands.")

    while not stop_event.is_set():
        command = vc.listen_for_command()
        process_voice_command(command)

def process_voice_command(command):
    """Handles commands from the website and controls navigation."""
    global stop_event, navigation_active

    if command == "start navigation":
        if not navigation_active:
            stop_event.clear()
            threading.Thread(target=start_navigation, args=(stop_event,)).start()
            return "Navigation started."
        return "Navigation is already running."
    
    elif command == "stop navigation":
        stop_event.set()
        navigation_active = False
        return "Navigation stopped."

    elif command == "where am i":
        return "You are currently in the main hallway."

    elif command == "turn left":
        return "Turning left."

    elif command == "turn right":
        return "Turning right."

    elif command == "move forward":
        return "Moving forward."

    elif command == "move backward":
        return "Moving backward."

    return "Command not recognized."

def generate_frames():
    """Handles video streaming to the website."""
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == "__main__":
    start_navigation(stop_event)
