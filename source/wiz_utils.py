import asyncio
from pywizlight import wizlight, PilotBuilder, discovery

async def wiz_discover():
    # Discover all bulbs in the network via broadcast datagram (UDP)
    # function takes the discovery object and returns a list of wizlight objects.
    bulbs = await discovery.discover_lights(broadcast_space="192.168.0.255")
    # Print the IP address of the bulb on index 0
    print(f"Bulb IP address: {bulbs[0].ip}")

    # Iterate over all returned bulbs
    list_of_bulbs = []
    for bulb in bulbs:
        dict_res = bulb.__dict__
        #append all details of bulb to list
        list_of_bulbs.append(dict_res)
        print(list_of_bulbs)
    
    return list_of_bulbs

"""BULB CONTROL"""

async def wiz_on(ipAddr,luminance):
    # set luminance 0-255
    light = wizlight(ipAddr)
    await light.turn_on(PilotBuilder(brightness = luminance))

async def wiz_off(ipAddr):
    # standard light
    light = wizlight(ipAddr)
    await light.turn_off()

async def wiz_onColour(ipAddr,r,g,b):
    # Set RGB values 0-255
    light = wizlight(ipAddr)
    await light.turn_on(PilotBuilder(rgb = (r, g, b)))

bulb_list = asyncio.run(wiz_discover())
print(bulb_list)

#{'ip': '192.168.0.100', 'port': 38899, 'state': None, 'mac': 'a8bb50ffce04', 'bulbtype': None, 'modelConfig': None, 'whiteRange': None, 'extwhiteRange': None, 'transport': None, 'protocol': None, 'history': 
#<pywizlight.bulb.WizHistory object at 0x000001F529BD65C8>, 'lock': <asyncio.locks.Lock object at 0x000001F529BD6708 [unlocked]>, 'loop': <_WindowsSelectorEventLoop running=True closed=False debug=False>, 'push_callback': None, 'response_method': None, 'response_future': None, 'push_cancel': None, 'last_push': -120.0, 'push_running': False}