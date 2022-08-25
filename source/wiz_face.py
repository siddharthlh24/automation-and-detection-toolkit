import asyncio
from wiz_utils import *
from error_codes import *
import time


async def arg_loop():
    list_of_bulbs = await wiz_discover()
    for bulb in list_of_bulbs:
        status = await wiz_on(bulb['ip'],255)
        print(status)
        time.sleep(5)
        status = await wiz_off(bulb['ip'])
        print(status)


loop = asyncio.run(arg_loop())
