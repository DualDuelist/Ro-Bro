import subprocess
import openai
import os
import speech_recognition as sr

# Set up the Speech Recognizer
recognizer = sr.Recognizer()

# Function to convert speech to text
def speech_to_text():
    with sr.Microphone() as source:
        print("I'm listening...")
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print("Error requesting results: {}".format(e))
            return None

def chatgpt(text):
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role" : "system" , "content" : "You're an assistant with an attitude problem.  You answer questions short and to the point, but will never hesitate to throw in a light verbal jab at your User, with delivery not dissimilar to Niles Crane from Frasier."},
	    {"role": "user" , "content" : text}
        ],
        temperature = 0.4,
    )
    return response['choices'][0]['message']['content']

# Function to generate text to speech with ESPEAK
def text_to_speech(text):
    try:
        # Generate text-to-speech and save to a temporary WAV file
        subprocess.run(['espeak', text, '-v', 'en-us+f3', '-w', 'temp.wav'])
        # Apply echo effect using sox
        subprocess.run(['sox', 'temp.wav', 'temp_echo.wav', 'echo', '0.6', '0.6', '20', '0.2'])
        # Play the audio using aplay
        subprocess.run(['aplay', 'temp_echo.wav'])
    finally:
        # Clean up: Delete temporary files
        os.remove('temp.wav')
        os.remove('temp_echo.wav')

# Main function
if __name__ == "__main__":
    while True:
        input("Press Enter to ask ChatGPT something...")
        text = speech_to_text()
        if text:
            print("\nYou said:", text, "\n")
            print("\nGenerating Response with ChatGPT\n")
            response = chatgpt(text)
            print("\nGenerating Voice with ESPEAK...\n")
            text_to_speech(response)
