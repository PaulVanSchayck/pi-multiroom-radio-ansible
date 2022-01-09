#!/usr/bin/env python3
import asyncio
import snapcast.control
import sys

loop = asyncio.get_event_loop()
server = loop.run_until_complete(snapcast.control.create_server(loop, 'localhost'))

if sys.argv[1] == 'all':
    group = next(item for item in server.groups if item.friendly_name == "Huis")

    # Loop over clients
    tasks = []
    for client_id in group.clients:
        client = server.client(client_id)
        tasks.append(client.set_muted(not client.muted))

    loop.run_until_complete(asyncio.gather(*tasks))
else:
    client = next(item for item in server.clients if item.friendly_name == sys.argv[1])
    loop.run_until_complete(client.set_muted(not client.muted))
