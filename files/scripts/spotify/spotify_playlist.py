#!/usr/bin/env python3
import spotipy
from librespot_token import token
import random
import sys

spotify = spotipy.Spotify(auth=token())

# TODO: Figure out way to get total
offset = random.randint(0, 30)

spotify.start_playback(device_id='b11bf19e3f65b4a1ada383e41f26dab5c503940e', context_uri=sys.argv[1], offset={'position':offset})