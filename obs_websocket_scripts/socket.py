#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests, events  # noqa: E402

class socket:

    def __init__(self):
        self.start = time.time()
        self.end = 0
        self.timer_done = 1
        self.neutral = 0
        self.happy = 0

    def on_switch(self, message):
        print(u"You changed the scene to {}".format(message.getSceneName()))


    def on_end(self,message):
        print(u"This scene ended {}".format(message.getName()))
        

    def vid_timer(self):
        self.end = time.time()
        elapsed = self.end - self.start
        if elapsed > 15:
            self.timer_done = 1
            self.start = time.time()
            self.neutral = not self.neutral
            self.happy = not self.happy

    def check_for_laughs(self):
        pass

    def check_for_negatives(self):
        pass

    def check_for_name(self):
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

            self.check_for_laughs()
            self.check_for_negatives()
            self.check_for_name()

            # timer at 15 seconds to wait for video to finish playing
            # need to have check laugh and check neg bypass that later
            try:
                if (self.neutral == 1) & (self.timer_done == 1):
                    ws.call(requests.SetCurrentScene("Neutral"))
                    self.timer_done = 0
                elif (self.happy == 1) & (self.timer_done == 1):
                    ws.call(requests.SetCurrentScene("Happy"))
                    self.timer_done = 0
                elif (negative == 1) & (self.timer_done == 1):
                    ws.call(requests.SetCurrentScene("Negative"))
                    self.timer_done = 0

                self.vid_timer()
                
            except KeyboardInterrupt:
                break

        ws.disconnect()


app = socket()
app.run()