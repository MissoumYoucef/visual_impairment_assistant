import cv2
import pytesseract
import pyttsx3
import speech_recognition as sr
from PIL import Image


# user 

# Initialize the text-to-speech engine

engine = pyttsx3.init()

# Initialize the speech recognizer

recognizer = sr.Recognizer()

# assume that we extract all information from QRCode (images, places, .... and so on)

# extract places fom QR codes example

Places = ['office', 'office1', 'office2']

while True:

    # System ask user where u want to go ?
    engine.say('Hi, where do you want to go?')
    engine.runAndWait()

    # Listen for the user's response
    with sr.Microphone() as source:
        print("Listening for your response...")
        audio = recognizer.listen(source)

    # Recognize the user's speech
    try:
        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)

        # Check if the user's response matches any of the places in Places list
        if any(place in user_input.lower() for place in Places):
            engine.say(f"Ok, i will guid.")
            engine.runAndWait()
            break  # Exit the loop if a place is recognized
        else:
            engine.say("Sorry, I did not understand. Please try again.")
            engine.runAndWait()

    except sr.UnknownValueError:
        engine.say("Sorry, I could not understand your speech. Please try again.")
        engine.runAndWait()
    except sr.RequestError as e:
        engine.say("Could not request results; {0}".format(e))
        engine.runAndWait()


# extract images fom QR codes example

# pytesseract.pytesseract.tesseract_cmd = 'C://T/tesseract.exe'  # your path may be different

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


image=Image.open('a2.jpg')

# Perform optical character recognition (OCR) on the image to extract text
text = pytesseract.image_to_string(image)
print(text)

# Define a dictionary mapping recognized text to audio guidance
text_to_audio_guidance = {
    "exit sign": "The exit sign is to your left. Follow the corridor to exit the building.",
    "wow": "The elevator is straight ahead. Press the button to call the elevator.",
    # Add more mappings for objects and locations in your workplace
}

# Convert the recognized text to lowercase for case-insensitive comparison
recognized_text_lower = text.lower()
# Check if the recognized text matches any object/location in the dictionary (case-insensitive)
if recognized_text_lower in text_to_audio_guidance:
    guidance = text_to_audio_guidance[recognized_text_lower]
    print(f"Recognized: {text}")
    print(f"Audio Guidance: {guidance}")
    engine.say(guidance)  # Speak the guidance
else:
    print("Object/location not recognized.")
    engine.say("Location not recognized.")  

# Clean up resources
engine.stop()
