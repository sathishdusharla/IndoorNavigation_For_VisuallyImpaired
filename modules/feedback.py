import pyttsx3
import serial

def audio_feedback(message):
    """Provide audio feedback using text-to-speech."""
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def haptic_feedback():
    """Provide haptic feedback using a connected device."""
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.write(b'1')  # Send signal to haptic device
    ser.close()