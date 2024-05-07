from __future__ import annotations
from typing import List
from shrillecho.artist.spotify_artist import SpotifyArtistUtil
from shrillecho.spotify.client import SpotifyClient
from shrillecho.track.spotify_track import SpotifyTrack
from shrillecho.types.album_types import Album
from shrillecho.types.artist_types import Artist
from shrillecho.types.playlist_types import Playlist
from shrillecho.types.soundcloud_types import User
from shrillecho.types.track_types import Track


class TracksController:
    
    """
        A class to encapsulate any collection of tracks
    """

    def __init__(self, sp: SpotifyClient, tracks: List[Track] = []):
        self.tracks: List[Track] = tracks
        self.liked_tracks: List[Track] = []
        self.unliked_tracks: List[Track] = []
        self._sp = sp

    @staticmethod
    async def create_from_playlist(sp: SpotifyClient, playlist: str):
        return TracksController(sp, tracks=await sp.playlist_tracks(playlist_id=playlist))
    
    @staticmethod
    async def create_from_album(sp: SpotifyClient, album: str):
        return TracksController(sp, tracks=await sp.album_tracks(album=album))

    async def load_playlist(self, playlist_id: str):
        self.tracks = await self._sp.playlist_tracks(playlist_id=playlist_id)
    
    async def load_likes(self):
        saved_tracks: List[Track] = await self._sp.current_user_saved_tracks()

        saved_track_map = set(saved_tracks)

        for track in self.tracks:

            if track in saved_track_map:
                track.liked = True
                self.liked_tracks.append(track)
            else:
                track.liked = False 
                self.unliked_tracks.append(track)



    async def load_album(self, album_id: str):
        self.tracks = await self._sp.album_tracks(album=album_id)

    async def write_tracks(self, name: str, user: str = "me") -> str:
    
        if user == "me":
            me: User = await self._sp.me()
            user = me.id

        tracks = SpotifyTrack.fetch_track_ids(self.tracks)
        
        playlist = await self._sp.user_playlist_create(user=user, name=name, public=False)
        limit = 50
        for i in range(0, len(tracks), limit):
            await self._sp.playlist_add_items(playlist['id'], tracks[i:i + limit])
        return playlist    

    async def artists(self, all_artists=False) -> List[Artist]:
        artist_ids_to_fetch = set()
        for track in self.tracks:
            if all_artists:
                for artist in track.artists:
                    artist_ids_to_fetch.add(artist.id)
            else:
                main_artist: Artist = SpotifyArtistUtil.determine_main_artist(track)
                if main_artist.id:
                    artist_ids_to_fetch.add(track.artists[0].id)

        playlist_artists: list[Artist] = await SpotifyArtistUtil.fetch_several_artists(self._sp, 
                                                                                   artist_ids=list(artist_ids_to_fetch))
        return playlist_artists

    async def genres(self) -> List[str]:
    
        playlist_artists: List[Artist] = self.artists()

        genre_set = set()

        for artist in playlist_artists:
            for genre in artist.genres:
                genre_set.add(genre)
        
        return list(genre_set)
    
    def __sub__(self, other: TracksController):
        other_track_sets = set(other.tracks) 
        return TracksController(sp=self._sp, 
                               tracks = [track for track in self.tracks if track not in other_track_sets], 
                               details=self.details)

    def __repr__(self):
        return f"{self.tracks}"
    
    
    def __and__(self, other):
        if isinstance(other, TracksController):
            self_set = set(self.tracks)
            other_set = set(other.tracks)
            return TracksController(sp=self._sp, tracks = self_set & other_set, details=self.details)
        return NotImplemented

    def __getitem__(self, index) -> Track:
        return self.tracks[index]
    
    def __len__(self):
        return len(self.tracks)
