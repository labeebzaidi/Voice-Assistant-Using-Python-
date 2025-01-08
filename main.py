import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "use your api key"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split("play ")[1].strip()
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song} in the music library.")
    elif "news" in c.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            print(f"API Call Status: {r.status_code}")  # Debug statement
            if r.status_code == 200:
                # Parse the JSON response
                data = r.json()
                print("API Call Successful!")  # Debug statement
                # Extract the articles
                articles = data.get('articles', [])
                print(f"Number of Articles: {len(articles)}")  # Debug statement
                
                # Print the headlines
                for article in articles:
                    print(article['title'])  # Debug statement
                    speak(article['title'])
            else:
                print(f"Failed to fetch news, status code: {r.status_code}")
                speak("Sorry, I couldn't fetch the news at the moment.")
        except Exception as e:
            print(f"Error fetching news: {e}")
            speak("Sorry, an error occurred while fetching the news.")

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for the wake word...")
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print(f"Error: {e}")
