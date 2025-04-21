import speech_recognition as sr
import pyttsx3
import threading

# Initialize text-to-speech engine globally
engine = pyttsx3.init()

def listen_for_command():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            try:
                audio = recognizer.listen(source, timeout=5)  # Wait max 5 seconds for input
                command = recognizer.recognize_google(audio)
                print(f"Command received: {command}")
                provide_audio_feedback(f"You said: {command}")
                process_command(command.lower())  # Call function to handle command
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                provide_audio_feedback("Sorry, I did not understand that.")
            except sr.RequestError:
                print("Could not connect to Google Speech Recognition service.")
                provide_audio_feedback("Could not connect to Google Speech Recognition service.")
            except sr.WaitTimeoutError:
                print("No command received. Listening again...")  # Avoid crashes if no input

def provide_audio_feedback(message):
    """Provides spoken feedback using text-to-speech."""
    if engine._inLoop:
        engine.endLoop()
    engine.say(message)
    engine.runAndWait()

def process_command(command):
    """Handles recognized commands."""
    if "stop" in command:
        print("Stopping the navigation system...")
        provide_audio_feedback("Stopping the navigation system.")
        exit(0)  # Exits the script safely
    elif "start" in command:
        print("Starting navigation...")
        provide_audio_feedback("Starting navigation.")
    else:
        print(f"Unknown command: {command}")
        provide_audio_feedback("Unknown command.")

# Run the speech recognition in a separate thread to avoid blocking
if __name__ == "__main__":
    command_thread = threading.Thread(target=listen_for_command, daemon=True)
    command_thread.start()

    while True:
        pass  # Keeps the main program running while listening in the background
