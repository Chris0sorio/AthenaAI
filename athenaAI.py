import speech_recognition as sr
from gtts import gTTS
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

import time



load_dotenv()
OPENAI_KEY = "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"

import openai
openai.api_key = OPENAI_KEY

# Function to convert text to speech with extended duration
def SpeakText(command, speed=1.25):

    start_time = time.time()  # Record the start time

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

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Speak to Text execution time: {elapsed_time:.2f}s")

    

# Initialize the recognizer
rInitializer = sr.Recognizer()

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    start_time = time.time()  # Record the start time
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
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Send to chatGPT execution time: {elapsed_time:.2f} seconds")
    return message

# Function to detect the wake word ("Athena")
def detect_wake_word(audio):
    # Record the start time
    start_time = time.time()  
    try:
        # Use the recognizer to convert audio to text
        command = rInitializer.recognize_google(audio)
        if "Athena" in command:
            return True
    except sr.UnknownValueError:
        pass
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Detect_wake_word execution time: {elapsed_time:.2f} seconds")
    return False

# Function to check if a kill term is spoken
def detect_kill_term(audio):
    start_time = time.time()  # Record the start time
    try:
        # Use the recognizer to convert audio to text
        command = rInitializer.recognize_google(audio)
        if "thank you" in command:
            print("Kill term detected. Exiting...")
            exit()
    except sr.UnknownValueError:
        pass
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Detect_kill_term execution time: {elapsed_time:.2f} seconds")

# Initialize messages
messages = [{"role": "user", "content": "Please act like Virtual assistant for users, your name is athena, you are a voice to voice assitant that utilizes chatGPT for better human interaction and help, and I the user am a sir."}]

while(1):
    
    with sr.Microphone() as source:
        print("Listening for 'Athena'...")
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
