#!/usr/bin/env python3
import requests
import sys

# Using librespot-java pass through to web-api
resp = requests.get(url="http://localhost:24879/web-api/v1/shows/{}/episodes?limit=1".format(sys.argv[1]))
data = resp.json()

uri = data['items'][0]['uri']

resp = requests.post(url="http://localhost:24879/player/load", params={"uri": uri, "play": "true"})

