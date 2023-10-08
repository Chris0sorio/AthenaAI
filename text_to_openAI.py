import speech_recognition as sr
from gtts import gTTS

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = "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"

import openai
openai.api_key = OPENAI_KEY

# Function to convert text to speech
def SpeakText(command):
    # Create a gTTS object
    tts = gTTS(text=command)
    # Save the speech to an audio file
    tts.save("output.mp3")
    # Play the saved audio file
    #os.system("mpg321 output.mp3")  # For Linux
    os.system("afplay output.mp3")  # For macOS
    #os.system("start output.mp3")   # For Windows

# Initialize the recognizer
rInitializer = sr.Recognizer()

def record_text():
    # Loop in case of error
    while True:
        try: 
            # Use the microphone as a source for input
            with sr.Microphone() as source2:
                # Prepare recognizer to receive input
                rInitializer.adjust_for_ambient_noise(source2, duration=0.2)
                print("I'm listening")
                # Listens for the user's input
                audio2 = rInitializer.listen(source2)
                # Using Google to recognize audio
                MyText = rInitializer.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = [{"role": "user", "content": "Please act like Jarvis from iron man."}]

while True:
    text = record_text()
    print("Wrote text:", text, "\n")
    print("Generating response...\n")
    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    print("Response:", response, "\n")
    print("Speaking...\n")
    SpeakText(response)
