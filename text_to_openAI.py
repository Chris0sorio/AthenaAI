import speech_recognition as sr
import pyttsx3
import rumps

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = "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"

import openai
openai.api_key = OPENAI_KEY

#Function to convert test to Speech
def SpeakText(command):

    #Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

#Initialize the recognizer
rInitializer = sr.Recognizer()

def record_text():
    #Loop in case of error
    while(1):
        try: 
            #use the microphone as source for input
            with sr.Microphone() as source2:
                #Prepare recognizer to recieve input
                rInitializer.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm listening")

                #listens for the user's input
                audio2 = rInitializer.listen(source2)

                #Using google to recognize audio
                MyText = rInitializer.recognize_google(audio2)

                return MyText

        except sr.RequestError as e:
            print ("Could not request results; {0}".format(e))
    
        except sr.UnknownValueError:
            print("Unknown error occured")

    return


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model = model,
        messages=messages,
        max_tokens = 100,
        n = 1,
        stop = None,
        temperature = 0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = [{"role": "user", "content": "Please act like Jarvis from iron man."}]
while(1):
    text = record_text()
    print("Wrote text: ", text)
    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    SpeakText(response)

    print("Response: ", response)