#!/usr/bin/env python3
import asyncio
import snapcast.control
import sys

loop = asyncio.get_event_loop()
server = loop.run_until_complete(snapcast.control.create_server(loop, 'localhost'))

group = next(item for item in server.groups if item.friendly_name == "Huis")

volume = group.volume + int(sys.argv[1])
loop.run_until_complete(group.set_volume(volume))