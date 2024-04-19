from dbus_next.aio import MessageBus
from dbus_next.service import (ServiceInterface,
                               method, dbus_property, signal)
from dbus_next import Variant, DBusError

import os
import discord
import asyncio
import setproctitle
import psutil

import nest_asyncio
nest_asyncio.apply()

client = discord.Client()

async def fetch_user(id):
    try:
        return await client.fetch_user(id)
    except discord.errors.NotFound:
        return discord.errors.NotFound

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
        
    sender = message.author

    if message.channel.type is discord.ChannelType.private:
        command = f"echo \"awesome.emit_signal('dcbus::notification', '{message.author.id}', '{sender}', '{message.content}')\" | awesome-client"
        os.system(command)

class DcBusInterface(ServiceInterface):
    def __init__(self):
        super().__init__('com.satou.dcbus')

    @method()
    async def Send(self, id: 's', message: 's'):
        user = await fetch_user(id)
        if message.endswith(".jpg") or message.endswith(".png") or message.endswith(".zip"):
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

def is_process_running(name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == name:
            return True
    return False

if __name__ == "__main__":
	if is_process_running('dcbus'):
		print("already running")
	else:
		setproctitle.setproctitle('dcbus')
		asyncio.run(main())
