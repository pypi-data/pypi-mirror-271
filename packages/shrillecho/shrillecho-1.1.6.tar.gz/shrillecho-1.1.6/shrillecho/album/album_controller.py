
from typing import List
from shrillecho.playlist.virtual_playlist import TracksController
from shrillecho.spotify.client import SpotifyClient
from shrillecho.types.album_types import Album
from shrillecho.types.track_types import Track


class AlbumController:

    def __init__(self, sp: SpotifyClient ,album: Album, tracks: TracksController):

        self._sp: SpotifyClient = sp
        self.album: Album = album
        self.album_tracks: TracksController = tracks
        
    @staticmethod
    async def create(sp: SpotifyClient, album_id: str = None, album: Album = None):

        if not album:
            album = await sp.album(album_id=album_id)
        
        if not album_id:
            album_id = album.id

        tracks = await TracksController.create_from_album(album_id)

        return AlbumController(sp=sp, album=album, tracks=tracks)
    
    async def internal_tracks(self) -> List[Track]:
        return self.album_tracks.tracks