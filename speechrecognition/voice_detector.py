import webrtcvad
import numpy as np


class voice_detector:


    def __init__(self, vad):
        self.vad = vad
        
    
    def check_audio(self, framex):
        sample_rate = 16000
        frame_duration = 10  

        frame = int(framex).to_bytes(2, "big") * int(sample_rate * frame_duration / 1000)
        
        return self.vad.is_speech(frame, sample_rate)
   



