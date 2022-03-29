#!/usr/bin/env python3
"""
perfect_playlist.py - Spotify playlist generation tool using a
                      Convolutional neural network
"""

__author__ = "Emma Dunsinger, Matthew O'Mara, Evan Noyes, Tommy Ngo"
__version__ = "0.1.0"
__license__ = "N/A"

import imageio
import spotipy
import os
import json
from spotipy.oauth2 import SpotifyClientCredentials

##Spotify API credentials here##
SPOTIPY_CLIENT_ID='9f4d5ba1da544502a6bdb038d16cf067'
SPOTIPY_CLIENT_SECRET='f54225b24200404baca25763718bd7c8'
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

def call_api():

    ## set environment varialbes
    os.environ['SPOTIPY_CLIENT_ID'] = str(SPOTIPY_CLIENT_ID)
    os.environ['SPOTIPY_CLIENT_SECRET'] = str(SPOTIPY_CLIENT_SECRET)
    os.environ['SPOTIPY_REDIRECT_URI'] = str(SPOTIPY_REDIRECT_URI)

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    results = sp.playlist_items('spotify:user:spotifycharts:playlist:37i9dQZEVXbMDoHDwVN2tF')
    # print(json.dumps(results, indent=4))

    # print(results.keys())
    items = results.get('items')
    print(json.dumps(items, indent=4))

    # print(items["name"])
    # for key, value in results.items():
    #     print(key, ' : ', value)

if __name__ == "__main__":
    input('press ENTER to start')
    call_api()
    input('press enter to exit')
    img = imageio.imread("images.png")
