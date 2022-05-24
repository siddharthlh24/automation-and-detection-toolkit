import asyncio
import time
import random
from pywizlight import wizlight, PilotBuilder, discovery

async def main():
    bulbs = await discovery.discover_lights(broadcast_space="192.168.0.255")
    for bulb in bulbs:
        #print(bulb.__dict__)
        print(bulb.__dict__)

        dict_res = bulb.__dict__
        ap = "a8bb50ffce04"

        if(dict_res['mac']==ap):
            light = wizlight(dict_res['ip'])

            #await light.turn_on(PilotBuilder())
            for i in range(10):
                await light.turn_on(PilotBuilder(rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
                time.sleep(2)
            await light.turn_off()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())