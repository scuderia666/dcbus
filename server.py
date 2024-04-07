from dbus_next.aio import MessageBus
from dbus_next.service import (ServiceInterface,
                               method, dbus_property, signal)
from dbus_next import Variant, DBusError

import os
import discord
import asyncio

import nest_asyncio
nest_asyncio.apply()

client = discord.Client()

async def fetch_user(id):
    try:
        return await client.fetch_user(id)
    except discord.errors.NotFound:
        return discord.errors.NotFound

class DcBusInterface(ServiceInterface):
    def __init__(self):
        super().__init__('com.satou.dcbus')

    @method()
    async def Send(self, id: 's', message: 's'):
        user = await fetch_user(id)
        if message.endswith(".jpg") or message.endswith(".png"):
            await user.send(file=discord.File(message))
        else:
            await user.send(message)
        print(message)

async def start_service():
    bus = await MessageBus().connect()
    interface = DcBusInterface()
    bus.export('/com/satou/dcbus', interface)
    await bus.request_name('com.satou.dcbus')

    await asyncio.sleep(2)

    await bus.wait_for_disconnect()

async def main():
    loop = asyncio.get_event_loop()

    print("starting dbus service")
    loop.create_task(start_service())

    print("starting discord client")
    loop.create_task(client.start(os.getenv("TOKEN")))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        await client.close()
    finally:
        await client.close()

asyncio.run(main())
