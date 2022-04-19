import unittest
import perfect_playlist

username = "31jvmeu7rifvdpcuitposjgjtz7i"
sp = perfect_playlist.get_spotify_client(username)

class TestCases(unittest.TestCase):

    def test_get_spotify_client(self):
        self.assertEqual("perfectplaylist", sp.current_user()["display_name"])

    def test_create_playlist(self):
        self.assertNotEqual("No playlist created!", perfect_playlist.create_playlist(sp, "test"))
    
    def test_get_playlist_id(self):
        self.assertNotEqual("No playlist ID found!", perfect_playlist.get_playlist_id(sp, "test"))

    """def test_get_song(self):
        sp = perfect_playlist.get_spotify_client(username)
        
        """

def main():
    tests = unittest.TestLoader().loadTestsFromTestCase(TestCases)
    unittest.TextTestRunner(verbosity=2).run(tests)

main()