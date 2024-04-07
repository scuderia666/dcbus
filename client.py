from dbus_next.aio import MessageBus
from dbus_next import Variant

import sys
import asyncio

async def client(msg):
    content = msg.split(None, 1)
    id = content[0]

    args = []
    if len(content) == 2:
        args = content[1].split()

    bus = await MessageBus().connect()

    introspection = await bus.introspect('com.satou.dcbus', '/com/satou/dcbus')

    proxy_object = bus.get_proxy_object('com.satou.dcbus',
                                    '/com/satou/dcbus',
                                    introspection)

    interface = proxy_object.get_interface('com.satou.dcbus')

    await interface.call_hello(id, content[1])

def main(exe, args):
    if args:
        asyncio.run(client(' '.join(args)))
    else:
        sys.exit('Usage: %s message...' % exe)

if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
