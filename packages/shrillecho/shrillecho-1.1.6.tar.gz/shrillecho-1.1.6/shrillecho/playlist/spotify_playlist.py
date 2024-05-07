import asyncio
import hashlib
from typing import List, Set

# Internal
from shrillecho.artist.spotify_artist import SpotifyArtistUtil
from shrillecho.playlist.virtual_playlist import TracksController
from shrillecho.spotify.client import SpotifyClient
from shrillecho.track.spotify_track import SpotifyTrack


# Type definitions
from shrillecho.types.artist_types import Artist
from shrillecho.types.playlist_types import PlaylistTrack, SimplifiedPlaylistObject
from shrillecho.types.track_types import Track
from shrillecho.utility.cache import cached
from shrillecho.utility.general_utility import get_id


class SpotifyPlaylist:

    # @staticmethod
    # async def get_genres_from_playlist(sp: SpotifyClient, playlist) -> List[str]:
    #     """ Get the set of genres from a playlist (unique)

    #         Args:
    #             sp (SpotifyClient): client
    #             playlist (str): playlist ID / URI / LINK
        
    #         Returns:
    #             List[str]: list of genres
    #     """
    #     tracks: List[Track] = await sp.playlist_tracks(playlist)

    #     genre_set = set()

    #     artist_ids_to_fetch = set()
    #     for track in tracks:
    #         if track.artists[0].id:
    #             artist_ids_to_fetch.add(track.artists[0].id)
               
    #     genre_set = set()

    #     playlist_artists: list[Artist] = await SpotifyArtistUtil.fetch_several_artists(sp, artist_ids=list(artist_ids_to_fetch))

    #     for artist in playlist_artists:
    #         for genre in artist.genres:
    #             genre_set.add(genre)
        
    #     return list(genre_set)


    @staticmethod
    async def write_songs_to_playlist(sp: SpotifyClient, name: str, track_list: List[Track], user: str) -> str:
        tracks = SpotifyTrack.fetch_track_ids(track_list)
        playlist = await sp.user_playlist_create(user=user, name=name, public=False)
        limit = 50
        for i in range(0, len(tracks), limit):
            await sp.playlist_add_items(playlist['id'], tracks[i:i + limit])
        return playlist
    
    @cached(cache_key_prefix="get_artist_tracks_from_playlistss", class_type=Track, expiry=3600)
    @staticmethod
    async def get_artist_tracks_from_playlist(sp: SpotifyClient, playlist: str) -> List[Track]:

        playlist_id = get_id("playlist", playlist)
        playlist_tracks: List[Track] = await sp.playlist_tracks(playlist_id=playlist_id)

        unique_artists = set()

        all_tracks: List[Track] = []

        for track in playlist_tracks:
            
            main_artist: Artist = await SpotifyArtistUtil.determine_main_artist(track)

            if main_artist.id not in unique_artists:
                print(f"fetching tracks for: {main_artist.name}")
                all_tracks.extend(await SpotifyArtistUtil.get_artist_tracks(sp, main_artist.id))

            unique_artists.add(main_artist.id)

        return all_tracks


    @staticmethod
    @cached(cache_key_prefix="like_filtered", class_type=Track, expiry=3600)
    async def removed_liked_tracks(sp, playlist_tracks: List[Track], liked_tracks: List[Track]) -> List[Track]:
        filtered_tracks: List[Track] = await SpotifyTrack.track_difference_liked(playlist_tracks=playlist_tracks, 
                                                                                liked_tracks=liked_tracks)
        for track in filtered_tracks:
            track.liked = False
        return filtered_tracks
    
    @staticmethod
    @cached(cache_key_prefix="load_playlist_liked", class_type=Track, expiry=3600)
    async def load_playlist_with_likes(sp, playlist_tracks, liked_tracks) -> List[Track]: 
    
        tasks = [SpotifyTrack.is_liked(track, liked_tracks=liked_tracks) for track in playlist_tracks]
        results = await asyncio.gather(*tasks)
        
        for track, liked in zip(playlist_tracks, results):
            track.liked = liked

        return playlist_tracks

    @staticmethod
    async def get_playlist_tracks_filtered(sp: SpotifyClient, playlist_id, get_non_liked=False) -> List[Track]:
        playlist: TracksController = await TracksController.create_from_playlist(sp, playlist_id)
        await playlist.load_likes()
        return playlist.unliked_tracks if get_non_liked else playlist.tracks