#!/usr/bin/env python3
import spotipy
from librespot_token import token

spotify = spotipy.Spotify(auth=token())

spotify.previous_track(device_id='b11bf19e3f65b4a1ada383e41f26dab5c503940e')
