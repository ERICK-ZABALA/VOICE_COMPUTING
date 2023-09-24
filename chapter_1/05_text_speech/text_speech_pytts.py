import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# change text as necessary
text=input('Type text to speak here: \n')

# speak output text
spoken_time=speak_text(text)