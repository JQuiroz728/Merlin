import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from time import ctime

"""
Voice Assistant application that uses Google's speech regonition library 
and text-to-speech API to process speech inputs and communicate with the user

Currently supports: 
 - Getting current time and date
 - Obtaining search results via Google
 - Getting directions for a given location via Google Maps
"""

r = sr.Recognizer()

def captureAudio(ask = False):
    with sr.Microphone() as source:
        if ask:
            merlinSpeak(ask)
        audio = r.listen(source)
        voiceData = ''
        try:
            voiceData = r.recognize_google(audio)
        except sr.UnknownValueError:
            merlinSpeak('Sorry I did not understand you')
        except sr.RequestError:
            merlinSpeak('Sorry service is currently down')
        return voiceData

def merlinSpeak(audioString):
    # Communicates through created audio files that are played to respond to user and are then removed from memory
    tts = gTTS(text = audioString, lang = 'en')
    r = random.randint(1, 10000000)
    audioFile = 'audio-' + str(r) + '.mp3'
    tts.save(audioFile)
    playsound.playsound(audioFile)
    print(audioString)
    os.remove(audioFile)

def respond(voiceData):
    # Currently only supports these few functionalities through specific word matching
    if 'what is your name' in voiceData:
        merlinSpeak('Hello my name is Merlin')
    if 'what time is it' in voiceData:
        merlinSpeak(ctime())
    if 'search' in voiceData:
        search = captureAudio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        merlinSpeak('Here are the results for ' + search)
    if 'find location' in voiceData:
        location = captureAudio('Where do you want to go?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        merlinSpeak('Here is the location of ' + location)
    if 'exit' in voiceData:
        exit()

time.sleep(1)
merlinSpeak('My name is Merlin. How can I help?') # Introduction
while 1:
    voiceData = captureAudio()
    respond(voiceData)
