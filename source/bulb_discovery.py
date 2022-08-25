import asyncio
import time
import random
from pywizlight import wizlight, PilotBuilder, discovery

async def main():
    print("yo")
    bulbs = await discovery.discover_lights(broadcast_space="192.168.0.255")
    print("boi")
    for bulb in bulbs:
        #print(bulb.__dict__)
        #print(bulb.__dict__)

        dict_res = bulb.__dict__
        ap = "a8bb50ffce04"

        if(dict_res['mac']==ap):
            light = wizlight(dict_res['ip'])

            #await light.turn_on(PilotBuilder())
            #for i in range(10):
            color_set = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            #await light.turn_on(PilotBuilder(rgb = color_set))
            await light.turn_on(PilotBuilder(cold_white = 100))
            state = await light.updateState()
            print(color_set)
            print("rgb", state.get_rgb())
            print("rgbw", state.get_state())
            print("www", state.get_brightness())
            time.sleep(5)
            await light.turn_off()
            state = await light.updateState()
            print("rgbw", state.get_state())
            #await light.turn_off()

loop = asyncio.run(main())
#loop.run_until_complete(main())