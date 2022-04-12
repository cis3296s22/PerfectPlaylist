Repository: https://github.com/cis3296s22/PerfectPlaylist
Branch Name: get_song


- Create function get_song
 > asks the user for input (as a string)
 > outputs 5 search results related to that string
 > asks for user input (1,2,3,4,5)
 > outputs song user has chosen 
	
	parameter "limit" (default=5), displays # of songs based on integer value
	song_list_str used for conjoining all song data

- TESTING 
 > Image included in branch 'get_song'
	documentation/branch-get_song/get_songTEST.png

   : Takes in user input "Adele", and prints five search results
   	asks for user input
   : User enters input '2' selecting 'Set Fire to Rain by Adele'	 

ERRORS:
	1. Entering certain integers as search string
	2. Invalid song input choice (assert having issues)


# Additions to main:
		
As of now for testing purposes calling the function that is being tested in each branch this case 'get_song'

- structured call_api() in multiple functions
 > setup_env_vars()
	moved all environment variables to seperate function
 > get_spotify_client() 
	simplified way to call a new client for each new function we add
 > get_top50


# For Creating a New Function
 Creating a spotify client has been simplified for the purpose of adding new functions
 At the top of each new function initialize a new spotify client
	'sp = get_spotify_client()'

A Documentation Folder has also been added for each new function
README on changes, and helping those understand each spotipy Call.










