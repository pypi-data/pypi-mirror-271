

import json
from typing import List
import requests
from shrillecho.spotify.client import SpotifyClient
from shrillecho.spotify.task_scheduler import TaskScheduler
from shrillecho.track.spotify_track import SpotifyTrack
from shrillecho.types.album_types import SimplifiedAlbum, SimplifiedTrack
from shrillecho.types.artist_types import Artist, FollowerCount
from shrillecho.types.track_types import Track
from shrillecho.utility.cache import cached


class ArtistController:


    def __init__(self, sp: SpotifyClient, artist: Artist):
        self._artist = artist
        self._sp = sp


    @staticmethod
    async def create(sp: SpotifyClient, artist_id: str = None, artist: Artist = None):

        if not artist:
            artist: Artist = await sp.artist(artist=artist_id)

        return ArtistController(sp=sp, artist=artist)
    
    
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
    
    async def get_artist_track_ids(self) -> List[str]:
        """ Return all tracks in the form of there ids

            Returns:
                List[str]: all artist tracks in for of ids
        """
      
        artist_albums: List[SimplifiedAlbum] = await self._sp.artist_albums(artist=self._artist)
        
        task_scheduluer = TaskScheduler()

        tasks = [
            (self._sp.album_tracks, (album.id,)) for album in artist_albums
        ]
    
        task_scheduluer.load_tasks(tasks)

        
        album_tracks: List[SimplifiedTrack] = await task_scheduluer.execute_tasks(batch_size=5)
     
   
        track_ids = [item.id for item in album_tracks]

        return track_ids

    async def get_artist_tracks(self, unique: bool = True) -> List[Track]:
        """ Return all tracks from an artist

            Args:
               unique: whether to remove duplicate tracks that appeared from the same release.
        
            Returns:
                int: followers (ML form)
        """
    
        tracks: List[Track] = await SpotifyTrack.fetch_several_tracks(sp=self._sp, track_ids= await self.get_artist_track_ids())

        if unique:
            return set(tracks)
        
        return tracks