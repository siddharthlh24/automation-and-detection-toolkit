import asyncio
from wiz_utils import *
from error_codes import *
import time
from functools import wraps
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

async def command_handler():
    #command_id
    cmdId = int(sys.argv[1])
    cmdArg = sys.argv[2:]
    if cmdId == commands.FACE_ON:
        await wiz_on(bulb_dict[cmdArg[0]],int(cmdArg[1]))
    elif cmdId == commands.FACE_OFF:
        await wiz_off(bulb_dict[cmdArg[0]])
    elif cmdId == commands.FACE_DISCOVER:
        print(" looking for bulbs, please wait")
        await refresh_bulbs()
    elif cmdId == commands.FACE_RGB:
        await wiz_onColour(bulb_dict[cmdArg[0]],int(cmdArg[1]),int(cmdArg[2]),int(cmdArg[3]))


async def main():
    await command_handler()
    time.sleep(0.1)

try:
    read_BulbsFromFile()
except:
    pass
print(bulb_dict)
loop = asyncio.new_event_loop()
loop.run_until_complete(main())