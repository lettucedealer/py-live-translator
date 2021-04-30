
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


        if (detector.check_audio(frame) is True):
            
            stream = sd.InputStream()

            

            recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
            sd.wait()
          
            write("audio.wav", recording, fs, sampwidth=2)

            with sr.WavFile("audio.wav") as source:
                audio = r.record(source)


            rec_audio = (r.recognize_google(audio))
            language = (change_language(rec_audio, googletrans.LANGUAGES, lang, language_changed))

            lang = language


            if (language_changed is False and language != "en"):
                print((translator.translate(rec_audio, dest=language).text))
                keyboard.write(translator.translate(rec_audio, dest=language).text)
                keyboard.press_and_release('ENTER')



