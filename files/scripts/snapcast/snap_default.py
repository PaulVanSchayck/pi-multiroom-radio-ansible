#!/usr/bin/env python3
import asyncio
import snapcast.control

loop = asyncio.get_event_loop()
server = loop.run_until_complete(snapcast.control.create_server(loop, 'localhost'))

living = next(item for item in server.clients if item.friendly_name == "Woonkamer")
kitchen = next(item for item in server.clients if item.friendly_name == "Keuken")

tasks = [
    living.set_volume(20),
    living.set_muted(False),
    kitchen.set_volume(20),
    kitchen.set_muted(False)
]

loop.run_until_complete(asyncio.gather(*tasks))
