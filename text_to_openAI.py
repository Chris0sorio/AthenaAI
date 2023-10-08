import speech_recognition as sr
from gtts import gTTS
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

import openai
openai.api_key = OPENAI_KEY

# Function to convert text to speech with extended duration
def SpeakText(command, speed=1.25):

    # Create a gTTS object
    tts = gTTS(text=command, lang='en', slow=False)

    # Save the speech to an audio file
    tts.save("output.mp3")

    # Load the audio file using pyDub
    audio = AudioSegment.from_mp3("output.mp3")

    # Adjust the speed of the audio
    adjusted_audio = audio.speedup(playback_speed=speed)

    # Play the adjusted audio
    play(adjusted_audio)
    

# Initialize the recognizer
rInitializer = sr.Recognizer()

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

# Function to detect the wake word ("Jarvis")
def detect_wake_word(audio):
    try:
        # Use the recognizer to convert audio to text
        command = rInitializer.recognize_google(audio)
        if "Jarvis" in command:
            return True
    except sr.UnknownValueError:
        pass
    return False

# Function to check if a kill term is spoken
def detect_kill_term(audio):
    try:
        # Use the recognizer to convert audio to text
        command = rInitializer.recognize_google(audio)
        if "thank you" in command:
            print("Kill term detected. Exiting...")
            exit()
    except sr.UnknownValueError:
        pass

# Initialize messages
messages = [{"role": "user", "content": "Please act like Jarvis from Iron Man. I am a sir."}]

while(1):
    
    with sr.Microphone() as source:
        print("Listening for 'Jarvis'...")
        audio = rInitializer.listen(source)
        
        if detect_wake_word(audio):
            print("Wake word detected. Listening for user command...")
            user_audio = rInitializer.listen(source, timeout=10)  # Listen for user command for up to 10 seconds
            
            try:
                # Use the recognizer to convert audio to text
                command = rInitializer.recognize_google(user_audio)
                print("User Command:", command)
                messages.append({"role": "user", "content": command})
                response = send_to_chatGPT(messages)
                print("Response:", response, "\n")
                print("Speaking...\n")
                SpeakText(response)
                detect_kill_term(user_audio)  # Check for the kill term
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
