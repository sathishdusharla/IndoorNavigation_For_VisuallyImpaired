import torch
import cv2

# Load the YOLOv5 model (use a smaller model for faster inference)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')

def detect_objects(image):
    """Detect objects in an image using YOLOv5."""
    # Resize the image to a smaller size for faster inference
    resized_image = cv2.resize(image, (320, 240))
    
    # Perform inference
    results = model(resized_image)
    
    # Process results
    detections = results.pandas().xyxy[0].to_dict(orient="records")
    for detection in detections:
        detection['name'] = results.names[int(detection['class'])]
    return detections