#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import speech_recognition as sr 
import pyttsx3 

import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests, events  # noqa: E402



class socket:

    def __init__(self):
        self.start = time.time()
        self.end = 0
        self.timer_done = 1
        self.neutral = 1
        self.happy = 0
        self.neutral_other = 0

    def on_switch(self, message):
        print(u"You changed the scene to {}".format(message.getSceneName()))


    def on_end(self,message):
        print(u"This scene ended {}".format(message.getName()))
        

    def vid_timer(self):
        self.end = time.time()
        elapsed = self.end - self.start
        if elapsed > 10:
            self.timer_done = 1
            self.start = time.time()
            self.neutral = not self.neutral
            self.neutral_other = not self.neutral_other
            print("done")
            
    
    def SpeakText(self,command): 
	# Initialize the engine 
        engine = pyttsx3.init() 
        engine.say(command) 
        engine.runAndWait() 

    def check_for_laughs(self):
        laugh = 0
        if(laugh):
            self.happy = 1
            self.neutral = 0
            self.neutral_other = 0
            self.timer_done == 1

    def check_for_negatives(self):
        pass

    def check_for_name(self):
        r = sr.Recognizer() 

        try: 
		
		# use the microphone as source for input. 
            with sr.Microphone() as source2: 
                
                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level 
                r.adjust_for_ambient_noise(source2, duration=0.2) 
                
                #listens for the user's input 
                audio2 = r.listen(source2) 
                
                # Using ggogle to recognize audio 
                MyText = r.recognize_google(audio2) 
                MyText = MyText.lower() 

                print("Did you say "+MyText) 
                if (MyText == "hey allison"):
                    self.SpeakText("pay attention somebody called on you") 
                    self.happy = 1 
                    self.timer_done = 1
                
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
            
        except sr.UnknownValueError: 
            print("unknown error occured") 
            pass

    def run(self):
        # connect to OBS
        host = "localhost"
        port = 4444
        password = "nwhacks"

        ws = obsws(host, port, password)
        ws.register(self.on_switch, events.SwitchScenes)
        ws.register(self.on_end, events.TransitionVideoEnd)
        ws.connect()

        self.neutral = 1
        self.happy = 0
        negative = 0

        while(1):

            #self.check_for_laughs()
            #self.check_for_negatives()
            #self.check_for_name()

            # timer at 15 seconds to wait for video to finish playing
            # need to have check laugh and check neg bypass that later
            try:
                if (self.neutral == 1) & (self.timer_done == 1):
                    ws.call(requests.SetCurrentScene("Neutral"))
                    self.timer_done = 0
                    print("neut")
                elif (self.happy == 1) & (self.timer_done == 1):
                    ws.call(requests.SetCurrentScene("Happy"))
                    self.timer_done = 0
                elif (negative == 1) & (self.timer_done == 1):
                    ws.call(requests.SetCurrentScene("Negative"))
                    self.timer_done = 0
                elif (self.neutral_other == 1) & (self.timer_done == 1):
                    ws.call(requests.SetCurrentScene("Neutral 2"))
                    self.timer_done = 0

                self.vid_timer()
                
            except KeyboardInterrupt:
                break

        ws.disconnect()


app = socket()
app.run()




