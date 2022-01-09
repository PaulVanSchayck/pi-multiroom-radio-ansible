#!/usr/bin/env python3
import spotipy
from librespot_token import token

spotify = spotipy.Spotify(auth=token())

state = spotify.current_playback()

if not state or not state['is_playing']:
    spotify.start_playback(device_id='b11bf19e3f65b4a1ada383e41f26dab5c503940e')
else:
    spotify.pause_playback(device_id='b11bf19e3f65b4a1ada383e41f26dab5c503940e')
