import asyncio
from wiz_utils import *
from error_codes import *
import time
from functools import wraps
import threading
from queue import Queue
import sys

## fix asyncio crying ##
from asyncio.proactor_events import _ProactorBasePipeTransport
 
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper
 
_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
"""fix yelling at me error end"""

#### problems fixed

bulb_dict = {}

def write_ToRamDict(mac,ip):
    bulb_dict.update({mac:ip})

def write_BulbsToFile(bulb_list):
    f1 = open("bulb.txt",'w')
    for item in bulb_list:
        f1.write("{}:{}\n".format(item['mac'],item['ip']))
        write_ToRamDict(item['mac'],item['ip'])
    f1.close()

def read_BulbsFromFile():
    f1 = open("bulb.txt",'r')
    for line in f1.readlines():
        mac,ip = line.split(":")[0],line.split(":")[1].replace("\n","")
        write_ToRamDict(mac,ip)
    f1.close()

async def refresh_bulbs():
    list_of_bulbs = await wiz_discover()
    write_BulbsToFile(list_of_bulbs)
    if(len(list_of_bulbs)==0):
        print("!!!!!!!!!!! no bulbs found")
    else:
        print(len(list_of_bulbs)," bulbs found")

# command id is 1 argument , cmdArgs have further arguments
async def command_handler(cmdId, cmdArg):
    if cmdId == commands.FACE_ON:
        await wiz_on(bulb_dict[cmdArg[0]],int(cmdArg[1]))
    elif cmdId == commands.FACE_OFF:
        await wiz_off(bulb_dict[cmdArg[0]])
    elif cmdId == commands.FACE_DISCOVER:
        print(" looking for bulbs, please wait")
        await refresh_bulbs()
    elif cmdId == commands.FACE_RGB:
        await wiz_onColour(bulb_dict[cmdArg[0]],int(cmdArg[1]),int(cmdArg[2]),int(cmdArg[3]))

global_bub_state = True
bulb_acl = "a8bb50d28225"
global_osTimer = None
global_queue = Queue(maxsize = 3)

async def toggle_diningLight_one():
    global global_bub_state
    if(global_bub_state):
        print("turning on")
        await command_handler(1,[bulb_acl,"100"])
        global_bub_state = False
    else:
        print("turning OFF")
        await command_handler(2,[bulb_acl])
        global_bub_state = True

async def loop_main(msg_qID):
    while(True):
        if(not global_queue.empty()):
            popped_msg = global_queue.get()
            if(popped_msg == "1"):
                await toggle_diningLight_one()

def run_interables():
    global global_osTimer
    while(True):
        print("time expired")
        global_queue.put("1")
        time.sleep(2)

def wiz_face_init(msg_qID):
    # attempt to pul ACLs from storage
    try:
        read_BulbsFromFile()
    except Exception as e:
        print("Exception occured",e)
        pass
    loop = asyncio.new_event_loop()
    print("came here")

    #start timer
    global global_osTimer
    thread = threading.Thread(target = run_interables)
    thread.start()

    loop.run_until_complete(loop_main(global_queue))
    print("came here ?")

wiz_face_init(global_queue)