import pyttsx3
import speech_recognition as sr
import openai

# Define your OpenAI GPT-3.5 API key
openai.api_key ='your_api_key'

# user

# Initialize the text-to-speech engine

engine = pyttsx3.init()

# Initialize the speech recognizer

recognizer = sr.Recognizer()

# assume that we extract all information from QRCode (images, places, .... and so on)

# extract places fom QR codes example

places = [
    {
        "name": "office",
        "description": """
                            To get to office 1 go toward along the corrider and take the elevator,
                            walk right you will find the office.
                            """,
    },
]



place_guide_description=''

# First section
# In this section we ask user about his distination
# User Side

while True:
    # System ask user where u want to go ?
    engine.say("Hi, where do you want to go?")
    engine.runAndWait()

    # Listen for the user's response
    with sr.Microphone() as source:
        print("Listening for your response...")
        audio = recognizer.listen(source)

    # Recognize the user's speech
    try:
        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)

        e = False
        for place in places:
            if place["name"] in user_input:
                place_guide_description=place["description"]## Accessing description of the place:
                engine.say(f"Ok, i am going to guide to ${place['name']}")
                engine.runAndWait()
                e = True
                break

        if e is False:
            engine.say("Sorry, I did not understand. Please try again.")
            engine.runAndWait()
        else:
            break

    except sr.UnknownValueError:
        engine.say("Sorry, I could not understand your speech. Please try again.")
        engine.runAndWait()
    except sr.RequestError as e:
        engine.say("Could not request results; {0}".format(e))
        engine.runAndWait()


# Second Part
# User's Camera will be launch and start detecting object and chatgpt try to advice user what can do.



# Example of function that using YOLO of detect from video and image objects AI,
# We assume that we used it 
# For demonstration, let's assume you have a list of detected objects

def detect_objects_from_video_or_image():
    return ['elevator', 'corridor','chair']  


detected_objects = detect_objects_from_video_or_image()


# generate_explanation
part_of_place_guide_description=place_guide_description.split(',')[0].strip()# will be = To get to office 1 go toward along the corrider and take the elevator,

def generate_explanation(msg_array, object_name):
    prompt = f"""
    we have a blind in a workplace and we want to guide him to a place so:
    act as Ai guider and Based on {part_of_place_guide_description}, try to Explain to him {object_name}.
    for example like this:
    "chair": "There is a chair nearby you can site down.",
    please just like this, don't generate any other sentence
    """
    msg_array.append(
       {"role": "user", "content": prompt}
    )
    response = openai.ChatCompletion.create(
       model="gpt-3.5-turbo",
       max_tokens=70,
       temperature=0.7,
       frequency_penalty=0.5,
       presence_penalty=0.5,
       messages=msg_array,
    )
    msg_array.append(response['choices'][0]['message'])
    response = response['choices'][0]['message']['content']
    return response


object_to_audio_guidance={}

# Generate explanations for each object/location

for object_name in detected_objects:
    explanation = generate_explanation([], object_name)
    object_to_audio_guidance[object_name] = explanation
    print(f"{object_name} Explanation: {explanation}")


# Example of object_to_audio_guidance fro chat gpt

# object_to_audio_guidance = {
#     'elevator': "There is an elevator in front of you. You can enter it to move between floors.",
#     'Chair': "There is a chair in front of you. You can sit down if needed."
# }


# Iterate through the detected objects and provide audio guidance if recognized


for obj_class in object_to_audio_guidance:
    guidance = object_to_audio_guidance[obj_class]
    print(f"Detected Object: {obj_class}")
    print(f"Audio Guidance: {guidance}")
    engine.say(guidance)  # Speak the guidance
    engine.runAndWait()


# Clean up resources
engine.stop()








