#!/usr/bin/env python3
"""
perfect_playlist.py - Spotify playlist generation tool using a
					  Convolutional neural network
"""

__author__ = "Emma Dunsinger, Matthew O'Mara, Evan Noyes, Tommy Ngo, Kyle Hrivnak"
__version__ = "0.1.0"
__license__ = "N/A"

# Library imports we need for the program.
import spotipy
import os
import logging

import spotipy.util as util

##Spotify API credentials here##
SPOTIPY_CLIENT_ID='3cfddad6d05a48c7a5abc03fbbb51b3b'
SPOTIPY_CLIENT_SECRET='8dc223b2ec4b44fda73b081b791a8401'
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

# Setting up a logger for the program so we can see what's going on.
logger = logging.getLogger('perfect_playlist')
logging.basicConfig(level='INFO') # Change this to DEBUG to see logging output, INFO to see less/only information relevant to the user.

# Now we need to create a few functions that will be useful for the program.

# Set up the environmental variables for the program.
def setup_env_vars():
	os.environ['SPOTIPY_CLIENT_ID'] = str(SPOTIPY_CLIENT_ID)
	os.environ['SPOTIPY_CLIENT_SECRET'] = str(SPOTIPY_CLIENT_SECRET)
	os.environ['SPOTIPY_REDIRECT_URI'] = str(SPOTIPY_REDIRECT_URI)

# First function will create a spotify client and return it.
def get_spotify_client(username):
	"""
	It creates a Spotify client using the spotipy library
	:return: spotipy.Spotify object
	"""
	setup_env_vars()
	scope = 'playlist-modify-public playlist-modify-private playlist-read-private' # We need to specify the scope of the program here, when you need a specific scope, you can add it here.
	token = util.prompt_for_user_token(username, scope)
	sp = spotipy.Spotify(auth=token)
	return sp

# Create a function that will create a playlist for the user.
def create_playlist(spotifyClient, playlistName):
	"""
	It creates a playlist for the user
	Modeled after: https://github.com/plamere/spotipy/blob/master/examples/create_playlist.py
	:param spotifyClient: spotipy.Spotify object
	:param playlistName: string
	:return: playlistID
	"""
	logger.debug("Creating playlist...")
	# Ask the user for a playlist name.
	try:
		playlist = spotifyClient.user_playlist_create(spotifyClient.me()['id'], playlistName)
		logger.debug("Playlist created.")
		return playlist["id"]
	except spotipy.exceptions.SpotifyException as e:
		logger.error("Error creating playlist: " + str(e))
		return "No playlist created!"

# Function to list all of the playlists for the user.
def list_playlists(spotifyClient):
	"""
	It lists first 50 playlists for the user.
	Modeled after: https://github.com/plamere/spotipy/blob/master/examples/my_playlists.py
	:param spotifyClient: spotipy.Spotify object
	:return: None
	"""
	logger.debug("Listing playlists...")
	print("\nPlaylists:\n")
	playlists = spotifyClient.user_playlists(spotifyClient.me()['id'])
	# Use enumerate to get the index of the playlist and have an easy way to display the playlist name.
	for i, playlist in enumerate(playlists['items']):
		print("%4d %s" % (i + 1 + playlists['offset'], playlist['name']))
	logger.debug("Playlists listed.")

# Function to list the top 50 tracks in spotify and list them.
def get_top50(spotifyClient):
	"""
	It lists the top 50 tracks in spotify
	:param spotifyClient: spotipy.Spotify object
	:return: None
	"""
	logger.debug("Listing top 50 tracks...")
	# We want to get them from this playlist: spotify:user:spotifycharts:playlist:37i9dQZEVXbMDoHDwVN2tF
	top50 = spotifyClient.playlist('spotify:user:spotifycharts:playlist:37i9dQZEVXbMDoHDwVN2tF')
	# We want to get the tracks from the playlist.
	print("\nSong - Artist - Album\n")
	for item in top50['tracks']['items']:
			print(
			item['track']['name'] + ' - ' +
			item['track']['artists'][0]['name'] + ' - ' +
			item['track']['album']['name']
			)
	print("\n### END OF TOP 50 PLAYLIST ###")
	logger.debug("Top 50 tracks listed.")

# Function to add a track to a playlist we specify.
def add_track_to_playlist(spotifyClient, playlistID, trackURI):
	"""
	It adds a track to a playlist
	:param spotifyClient: spotipy.Spotify object
	:param playlistID: string
	:param trackURI: string
	:return: None
	"""
	logger.debug("Adding track to playlist...")
	# We want to add the track to the playlist.
	spotifyClient.user_playlist_add_tracks(spotifyClient.me()['id'], playlistID, [trackURI])
	logger.debug("Track added to playlist.")

# Function to get playlist ID from a given playlist name.
def get_playlist_id(spotifyClient, playlistName):
	"""
	It gets the playlist ID from a given playlist name
	:param spotifyClient: spotipy.Spotify object
	:param playlistName: string
	:return: playlistID
	"""
	logger.debug("Getting playlist ID...")
	# We want to get the playlist ID from the playlist name.
	playlists = spotifyClient.user_playlists(spotifyClient.me()['id'])
	for playlist in playlists['items']:
		if playlist['name'] == playlistName:
			return playlist['id']
	logger.debug("Playlist ID retrieved.")
	return "No playlist ID found!"

# Function which will get the song name from the track URI, after prompting the user for the track name.
def get_song(spotifyClient):
	"""
	It gets the song name from the track URI
	:param spotifyClient: spotipy.Spotify object
	:return: trackURI
	"""
	songName = input("Type in a song title to search: ")
	sp = spotifyClient

	results = sp.search(q = songName, type='track', limit=5)
	possible_songs = results.get('tracks').get('items')

	song_list_str = ''
	for i, song in enumerate(possible_songs):
		song_list_str += f'{i+1}. {song["name"]} by {song["artists"][0]["name"]}\n'
	song_selection = input(f'\n{song_list_str}\nEnter the number of the song you want to select: ')
	assert song_selection.isdigit(), 'Please enter a number'
	assert int(song_selection) <= len(possible_songs), 'Please enter a number between 1 and {}'.format(len(possible_songs))
	selected_song = possible_songs[int(song_selection)-1]
	print(f'[option={int(song_selection)}, query="{songName}"]')
	print(f'>>>\n>>> {selected_song["name"]} by {selected_song["artists"][0]["name"]}\n>>>')
	# Get the track URI from the track name.
	return selected_song['uri']

# Main function. This is where the program starts/interacts with the user from the beginning.
def main(username):
	# We need to create a spotify client and save it to a variable, then pass it to the other functions as needed.
	logger.debug("Creating Spotify client...")
	sp = get_spotify_client(username)
	logger.debug("Spotify client created.")

	# Create a loop to get input from user and then choose an option.
	while True:
		# Ask the user what they want to do.
		print("\nWhat would you like to do?")
		print("1. Create a playlist")
		print("2. List your playlists")
		print("3. List the top 50 tracks")
		print("4. Add a track to a playlist")
		print("5. Exit")
		choice = input("\nEnter your choice: ")

		# If the user chooses to create a playlist, we need to ask them for a playlist name.
		if choice == "1":
			playlistName = input("Enter a name for your playlist: ")
			playlistID = create_playlist(sp, playlistName)
			if "No playlist created!" in playlistID:
				print("No playlist created!")
			else:
				print("Playlist created! ID: " + playlistID)
		elif choice == "2":
			list_playlists(sp)
		elif choice == "3":
			get_top50(sp)
		elif choice == "4":
			playlistName = input("Enter the name of the playlist you want to add the track to: ")
			playlistID = get_playlist_id(sp, playlistName)
			if "No playlist ID found!" in playlistID:
				print("No playlist ID found!")
			else:
				trackURI = get_song(sp)
				add_track_to_playlist(sp, playlistID, trackURI)
				print("Track added to playlist!")
		elif choice == "5":
			print("\nExiting... Thanks for using Perfect Playlist!")
			break
		# If the user enters an invalid choice, we need to tell them and then ask them again.
		else:
			print("Invalid choice. Please try again.")

	pass

# This function is used to get the top 50 songs from the Spotify charts.
if __name__ == "__main__":
	# We need to call the main function, but in order to do that we would require the user to enter their username.
	# We can't do that from the command line, so we need to ask the user for their username.
	# Bear in mind this is only relevant the first time the program is run/if user credentials are deleted.
	username = input("Enter your Spotify username: ")

	# Call the main function with the username as an argument.
	logger.debug("Starting program...")
	main(username)

	pass
