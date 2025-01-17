import pyttsx3

engine = pyttsx3.init()

def speak_feedback(message):
    engine.say(message)
    engine.runAndWait()
