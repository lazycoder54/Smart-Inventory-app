import speech_recognition as sr
import time
from flask import Blueprint, jsonify

inventory_bp = Blueprint('inventory_bp', __name__)
stop_flag = False

def stop_recognition():
    global stop_flag
    stop_flag = True
    
def recognize_speech_from_mic():
    global stop_flag
    stop_flag = False
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            start_time = time.time()
            audio = None

            while not stop_flag and (time.time() - start_time) < 50:  
                try:
                    audio = recognizer.listen(source, timeout=50, phrase_time_limit=50)
                    break
                except sr.WaitTimeoutError:
                    continue

            if stop_flag:
                print("Stopped listening.")
                return None

            print("Processing your voice command...")
            command = recognizer.recognize_google(audio)
            print(f"Command recognized: {command}")
            return command

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


