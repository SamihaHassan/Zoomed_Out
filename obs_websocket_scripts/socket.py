
# import simpleobsws
# import asyncio


# loop = asyncio.get_event_loop()
# ws = simpleobsws.obsws(host='localhost', port=4444, password='nwhacks', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

# async def make_request():
#     await ws.connect() # Make the connection to OBS-Websocket
#     result = await ws.call('GetVersion') # We get the current OBS version. More request data is not required
#     print(result) # Print the raw json output of the GetVersion request
#     await asyncio.sleep(1)
#     data = {'source':'test_source', 'volume':0.5}
#     result = await ws.call('SetVolume', data) # Make a request with the given data
#     print(result)
#     await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.

# loop.run_until_complete(make_request())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402


host = "localhost"
port = 4444
password = "nwhacks"

ws = obsws(host, port, password)
ws.connect()

try:
    scenes = ws.call(requests.GetSceneList())
    for s in scenes.getScenes():
        name = s['name']
        print(u"Switching to {}".format(name))
        ws.call(requests.SetCurrentScene(name))
        time.sleep(2)

    print("End of list")

except KeyboardInterrupt:
    pass

ws.disconnect()