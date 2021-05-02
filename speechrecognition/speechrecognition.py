
import speech_recognition as sr
import sounddevice as sd
from wavio import write
import googletrans
from googletrans import Translator
import webrtcvad
from voice_detector import voice_detector
import wave
import numpy as np
import keyboard
from threading import Thread

r = sr.Recognizer()

vad = webrtcvad.Vad(2)

detector = voice_detector(vad)

toggler = False

def change_language(recording, languages, previous_lang, language_changed):
    split_recording = recording.split()
    if split_recording[0] == "change" and split_recording[1] == "language" and len(split_recording) == 3:
        for key, value in languages.items():
            if split_recording[2].lower() == value:
                language_changed = True
                print("language has been changed")
                return key
                
    else:
        language_changed = False
        return previous_lang

def toggle(recording, current_value):
    split_recording = recording.split()
    if (split_recording[0] == "toggle" and len(split_recording) == 2):
        if split_recording[1] == "on":
            current_value = True
            print("Toggled ON")
            return current_value
        if split_recording[1] == "off":
            current_value = False
            print("Toggled OFF")
            return current_value
    else:
        return current_value
            


keyer = input("What key does your platform use to chat?\nWrite it as a capital (if it's the enter key, write ENTER, if its space write SPACE):")



        


fs = 44100

duration = 5 
pre_duration = 0.1

lang = "en"

translator = Translator()





while True:



    language_changed = False

    pre_recording = sd.rec(int(pre_duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write("pre_audio.wav", pre_recording, fs, sampwidth=2)

    file = wave.open("pre_audio.wav", "rb")
    frames = file.readframes(file.getnframes())

    for frame in frames:

        try:
            if (detector.check_audio(frame) is True):
            
                stream = sd.InputStream()

            

                recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
                sd.wait()
          
                write("audio.wav", recording, fs, sampwidth=2)

                with sr.WavFile("audio.wav") as source:
                    audio = r.record(source)


                rec_audio = (r.recognize_google(audio))

                toggler = toggle(rec_audio, toggler)
            

                if toggler is True:
                    language = (change_language(rec_audio, googletrans.LANGUAGES, lang, language_changed))
                

                    lang = language


                    if (language_changed is False and language != "en" and toggler is True):
                        print((translator.translate(rec_audio, dest=language).text))
                        keyboard.press_and_release(keyer)
                        keyboard.write(translator.translate(rec_audio, dest=language).text)
                        keyboard.press_and_release('ENTER')
        except:
            print("exception encountered")


