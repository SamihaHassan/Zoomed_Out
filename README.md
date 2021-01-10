# Zoomed_Out
nwHacks 2021 Project

## Purpose

Feeling that Zoom fatigue, constantly zoning out during long meetings without ever needing to speak up, want to support your prof with your smilling face but also want to chill in PJs? Look no further, ZoomedOut has got your back.

Set up this virtual camera and always look your best for your fellow peers. Our intelligent virtual camera will react in real time to what's happenining in your meeting so you cry or laugh on time without having to actively pay attention. Use this saved time to make 2021 as productive as possible. Our program also will alert you if your name has been mentioned and save the key points of the meeting for you to review later. 

ZoomedOut is also great for turning on your camera for your classes to support your professors so they don't have to stare into the voice while teaching. Show your smilling, appreciative self looking your best all from the comfort of your bed. 

![zoomedout](zoomedout.png)

## Dependencies

Download OBS and the following plugins to use the virtual camera feature

https://obsproject.com/

https://obsproject.com/forum/threads/advanced-scene-switcher.48264/

https://obsproject.com/forum/resources/obs-websocket-remote-control-obs-studio-from-websockets.466/

https://obsproject.com/forum/resources/obs-virtualcam.949/

We are using a websocket to control remotely the clips being played via OBS, the software that allows us to use the virtual camera. Once you download OBS, upload a few neutral face clips, a happy/laughing clip and sad faced clip. The script `socket.py` will allow you to connect to OBS and then control the scene names to play.


### Python Packages

`pip install` from the requirements.txt

### Google Cloud 
- Google Vision: We first tried to implement emotion recognition using Google Vision but we were unable to get access properly
- Dialog Flow: We used Dialogflow to detect when your name has been called. We decided to use machine learning so that the bot can determine when to notify you whether it's your name or your job position being mentioned. The implementation can be found in the branch integration, via simple chat bot for now. 

### OpenCV
We are using openCV to capture the screen with the video call and detect the emotions of those in the call. This will trigger the OBS clips to play depending on the emotion detected. For example, if everyone in the call were to laugh, this will trigger OBS websocket to start the laughing clip. When the neutral emotion is detected, the OBS websocket will cycle between different clips of your neutral face. 


