# /index.py
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
import sys
import time
from multiprocessing import Process, Value
import logging
import speech_recognition as sr
import pyttsx3


import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests, events  # noqa: E402

app = Flask(__name__)


@app.route('/')
def index():
    global p
    p = Process(target=loop)
    p.start()
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    if data['queryResult']['queryText'] == 'allison':
        reply = {
            "fulfillmentText": "Ok. Tickets booked successfully.",
        }
        return jsonify(reply)

    elif data['queryResult']['queryText'] == 'no':
        reply = {
            "fulfillmentText": "Ok. Booking cancelled.",
        }
        return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    app.logger.warning("newss")
    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message(message_in):
    message = message_in
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message":  fulfillment_text}
    print(os.getenv('DIALOGFLOW_PROJECT_ID'))
    return jsonify(response_text)

class socket:
    def __init__(self):
        self.start = time.time()
        self.end = 0
        self.timer_done = 1
        self.neutral = 0
        self.happy = 0

    def on_switch(self, message):

        print(u"You changed the scene to {}".format(
            message.getSceneName()))
        app.logger.warning(u"You changed the scene to {}".format(
            message.getSceneName()))

    def on_end(self, message):
        print(u"This scene ended {}".format(
            message.getName()))
        app.logger.warning(u"This scene ended {}".format(
            message.getName()))

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
                app.logger.warning("Did you say "+MyText) 
                returned = send_message(MyText)
                app.logger.warning(returned) 
                # engine = pyttsx3.init('dummy')
                # engine.say("pay attention")
                # engine.runAndWait()
                
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
            
        except sr.UnknownValueError: 
            print("unknown error occured") 
            pass

        

    def run(self):
        global r
        r = sr.Recognizer()

        # connect to OBS
        host = "localhost"
        port = 4444
        password = "nwhacks"

        ws = obsws(host, port, password)
        ws.register(self.on_switch, events.SwitchScenes)
        ws.register(self.on_end, events.TransitionVideoEnd)
        ws.connect()

        print("connected", file=sys.stderr)

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


def loop():
    app.logger.warning("OBS")
    sockobs = socket()
    sockobs.run()


# run Flask app
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    p.join()
