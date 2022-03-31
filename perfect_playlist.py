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
import typer

from spotipy.oauth2 import SpotifyClientCredentials

##Spotify API credentials here##
SPOTIPY_CLIENT_ID='9f4d5ba1da544502a6bdb038d16cf067'
SPOTIPY_CLIENT_SECRET='f54225b24200404baca25763718bd7c8'
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

def get_top50():
    sp = get_spotify_client()
    results = sp.playlist('spotify:user:spotifycharts:playlist:37i9dQZEVXbMDoHDwVN2tF')

    print("\nSong - Artist - Album\n")
    for item in results['tracks']['items']:
            print(
            item['track']['name'] + ' - ' +
            item['track']['artists'][0]['name'] + ' - ' +
            item['track']['album']['name']
            )
    print("\n### END OF TOP 50 PLAYLIST ### \n")



def get_spotify_client() -> spotipy.Spotify:
    """
    It creates a Spotify client using the spotipy library
    :return: spotipy.Spotify object
    """
    setup_env_vars()
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def setup_env_vars():
    ## set environment varialbes
    os.environ['SPOTIPY_CLIENT_ID'] = str(SPOTIPY_CLIENT_ID)
    os.environ['SPOTIPY_CLIENT_SECRET'] = str(SPOTIPY_CLIENT_SECRET)
    os.environ['SPOTIPY_REDIRECT_URI'] = str(SPOTIPY_REDIRECT_URI)


def get_song():
    songName = input("Type in a song title to search:  ")
    sp = get_spotify_client()

    results = sp.search(q = songName, type='track', limit=5)
    possible_songs = results.get('tracks').get('items')

    song_list_str = ''
    for i, song in enumerate(possible_songs):
        song_list_str += f'{i+1}. {song["name"]} by {song["artists"][0]["name"]}\n'
    song_selection = input(f'\n{song_list_str}\n\nEnter the number of the song you want to select: ')
    assert song_selection.isdigit(), 'Please enter a number'
    assert int(song_selection) <= len(possible_songs), 'Please enter a number between 1 and {}'.format(len(possible_songs))
    selected_song = possible_songs[int(song_selection)-1]
    print(f'[option={int(song_selection)}, query="{songName}"]')
    print(f'>>>\n>>> {selected_song["name"]} by {selected_song["artists"][0]["name"]}\n>>>\n')



    #TO BE COMPLETED

if __name__ == "__main__":
    ##img = imageio.imread("images.png")
    input('press ENTER to start\n')

    ## START of get_top50 (formerly call_api)
    '''
    get_top50()
    '''
    ## START of get song
    get_song()



    input('press enter to exit')
