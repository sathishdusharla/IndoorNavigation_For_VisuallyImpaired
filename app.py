from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import threading
import modules.obstacle_detection as od
import pyttsx3

app = Flask(__name__)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine_lock = threading.Lock()
detection_active = True  
last_command = ""
last_frame_hash = None  

def provide_audio_feedback(text):
    """Speaks only if the command is new to avoid repetition."""
    global last_command
    if text == last_command:
        return  
    last_command = text  

    def speak():
        with engine_lock:
            engine.say(text)
            engine.runAndWait()

    threading.Thread(target=speak, daemon=True).start()

def is_camera_moved(frame):
    """Detects if the camera has moved based on image hash."""
    global last_frame_hash
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_hash = hash(gray.tobytes())  

    if last_frame_hash is None or frame_hash != last_frame_hash:
        last_frame_hash = frame_hash
        return True  
    return False  

def process_image(image_data):
    """Processes the uploaded image and provides navigation feedback."""
    global detection_active
    if not detection_active:
        return "Detection is stopped."

    image_data = image_data.split(",")[1]  
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if not is_camera_moved(frame):
        return "No movement detected. Waiting for change."

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    obstacles = od.detect_objects(blurred_frame)
    response = "Path is clear. You may proceed."

    left_clear, right_clear = True, True  

    if obstacles:
        for obj in obstacles:
            name = obj['name']
            x1, _, x2, _ = int(obj['xmin']), int(obj['ymin']), int(obj['xmax']), int(obj['ymax'])
            frame_center = frame.shape[1] // 2
            object_center = (x1 + x2) // 2
            side = "left" if object_center < frame_center else "right"

            if side == "left":
                left_clear = False
            else:
                right_clear = False

            response = f"Warning! {name} detected on your {side}."

    if left_clear and not right_clear:
        response += " Move to the left."
    elif right_clear and not left_clear:
        response += " Move to the right."
    elif not left_clear and not right_clear:
        response += " Path is blocked. Stop or move backward."

    provide_audio_feedback(response)
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Receives an image and processes it for object detection."""
    data = request.json
    image_data = data.get("image")
    if not image_data:
        return jsonify({"error": "No image provided."}), 400

    response = process_image(image_data)
    return jsonify({"message": response})

@app.route('/toggle_detection', methods=['POST'])
def toggle_detection():
    """Toggles object detection on or off."""
    global detection_active
    detection_active = not detection_active
    status = "started" if detection_active else "stopped"
    provide_audio_feedback(f"Detection {status}.")
    return jsonify({"message": f"Detection {status}."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
