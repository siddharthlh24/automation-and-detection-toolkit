import asyncio
from pywizlight import wizlight, PilotBuilder, discovery
from error_codes import *

async def wiz_discover():
    # Discover all bulbs in the network via broadcast datagram (UDP)
    # function takes the discovery object and returns a list of wizlight objects.
    bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    # Print the IP address of the bulb on index 0
    #print(f"Bulb IP address: {bulbs[0].ip}")

    # Iterate over all returned bulbs
    list_of_bulbs = []
    for bulb in bulbs:
        dict_res = bulb.__dict__
        #append all details of bulb to list
        list_of_bulbs.append(dict_res)
        print(list_of_bulbs)
    
    return list_of_bulbs

"""BULB CONTROL"""

# get bulb state
async def bulb_status(light_obj):
    state = await light_obj.updateState()
    bulb_status = state.get_state()
    return bulb_status

# set luminance 0-255
async def wiz_on(ipAddr,luminance):
    opStatus = WIZ_ERROR
    light = wizlight(ipAddr)
    await light.turn_on(PilotBuilder(cold_white = luminance))
    if(True == await bulb_status(light)):
        opStatus = WIZ_OK
    return opStatus
    
# standard light off
async def wiz_off(ipAddr):
    opStatus = WIZ_ERROR
    light = wizlight(ipAddr)
    await light.turn_off()
    if(False == await bulb_status(light)):
        opStatus = WIZ_OK
    return opStatus

# Set RGB values 0-255
async def wiz_onColour(ipAddr,r,g,b):
    opStatus = WIZ_ERROR
    light = wizlight(ipAddr)
    await light.turn_on(PilotBuilder(rgb = (r, g, b)))
    if(True == await bulb_status(light)):
        opStatus = WIZ_OK
    return opStatus