

import json
import requests
from shrillecho.spotify.client import SpotifyClient
from shrillecho.types.artist_types import Artist, FollowerCount
from shrillecho.utility.cache import cached
from shrillecho.utility.general_utility import get_id


class ArtistController:

    def __init__(self, sp: SpotifyClient, artist: Artist):
        self._sp: SpotifyClient = sp
        self.artist: Artist = artist

    @cached(cache_key_prefix="followers", class_type=FollowerCount, expiry=3600)
    async def followers(self) -> int:
        """ the number of followers (ML form)

            Args:
                track (Artist): The artist to get the followers of (ML form)
        
            Returns:
                int: followers (ML form)
        """
        data = {"artist": self.artist.id}
        followers_call = requests.post("http://localhost:8002/ml", json=data)
        followers = followers_call.json()
        return FollowerCount.from_json(json.dumps(followers))
    
