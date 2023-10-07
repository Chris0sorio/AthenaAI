import speech_recognition as sr
import pyttsx3

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

def output_text(text):
    file = open("output_speech_text.txt", "a")
    file.write(text)
    file.write("\n")
    file.close()
    return

while(1):
    text = record_text()
    output_text(text)
    
    print("Wrote text: ", text)

