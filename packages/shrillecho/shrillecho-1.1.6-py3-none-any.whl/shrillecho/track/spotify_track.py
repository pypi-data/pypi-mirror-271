from typing import List

import spotipy
import requests

# Internal
from shrillecho.spotify.client import SpotifyClient
from shrillecho.types.album_types import Album, SeveralAlbums
from shrillecho.types.playlist_types import Playlist, SimplifiedPlaylistObject
from shrillecho.types.track_types import SeveralTracks, Track
from shrillecho.utility.archive_maybe_delete.spotify_client import SpotifyClientGlitch

class SpotifyTrack:


    @staticmethod
    def is_duplicate_track(track_a: Track, track_b: Track):
        pass

    @staticmethod
    async def fetch_several_albums(sp: SpotifyClient, album_ids: List[str], batch_size: int = 20) -> List[Album]:
        albums: List[Album] = []
        for i in range(0, len(album_ids), batch_size):
            chunk = album_ids[i:i + batch_size]
            more_albums: SeveralAlbums = await sp.albums(chunk)
            albums.extend(more_albums.albums)
        return albums
        

    @staticmethod
    async def fetch_several_tracks(sp: SpotifyClient, track_ids: List[str], batch_size: int = 50) -> List[Track]:
        tracks: List[Track] = []
        for i in range(0, len(track_ids), batch_size):
            chunk = track_ids[i:i + batch_size]
            more_tracks: List[Track] = await sp.tracks(chunk)
            tracks.extend(more_tracks)
        return tracks

    @staticmethod
    async def fetch_all_user_public_tracks(sp: SpotifyClient, user: str) -> List[Track]:
        tracks: List[Track] = []
        playlists: List[SimplifiedPlaylistObject] = await sp.user_playlists(user=user, batch=True, chunk_size=25)
        for playlist in playlists:
            tracks.extend(await sp.playlist_tracks(playlist_id=playlist.id, batch=True, chunk_size=25))
        return tracks

    @staticmethod
    def track_difference(track_list_A: List[Track], track_list_B: List[Track]) -> List[Track]:
        """ Given track list A and B, compute A - B i.e all tracks in A minus all the tracks from B.

            Args:
              track_list_A (List[Track]): list to be removed from
              track_list_B (List[Track]): list to choose which songs to remove
        
            Returns:
                List[Track]: A-B tracks
        """
        metadata_dict: dict = {}
        local_or_removed = 0
        for track_b in track_list_B:
           
            try:
                key = (track_b.artists[0].id, track_b.name) 
            
                if key not in metadata_dict:
                    metadata_dict[key] = set()
                metadata_dict[key].add(track_b.external_ids.isrc)
            except:
                local_or_removed +=1
                continue
           
        filtered_a = []

        x = 0
 
        for track_a in track_list_A:
            try:
                key = (track_a.artists[0].id ,track_a.name ) 
                if any(track_a.external_ids.isrc in isrc for isrc in metadata_dict.get(key, set())):
                    continue 
                if key not in metadata_dict:
                    filtered_a.append(track_a)
                    continue
                x +=1
                print(f'isrc miss: {track_a.name}')
            except:
                continue
            
        return filtered_a
    
        
    @staticmethod
    def fetch_track_ids(tracks: List[Track]) -> List[str]:
        """
            Given a list of tracks return a list of the ids only
        """

        ids = []
        for track in tracks:
            if track.id:
                ids.append(track.id)
        return ids
    

    @staticmethod
    def clean_tracks(tracks: List[Track]) -> List[Track]:
        """
            Given a list of tracks remove all tracks that dont have ISRC
        """

        local_removed_copyright = 0
        cleaned_tracks: List[Track] = []
        for track in tracks:
            if track.external_ids.isrc:
                if track.artists[0].name == "heyamina":
                    
                    print(track.external_ids.isrc)
                cleaned_tracks.append(track)
            else:
                local_removed_copyright += 1

        print(f'local_removed_copyright: {local_removed_copyright}')
        return cleaned_tracks

    @staticmethod
    async def track_difference_liked(playlist_tracks: List[Track], liked_tracks: List[Track]) -> List[Track]:
        return SpotifyTrack.track_difference(playlist_tracks, liked_tracks)
    
    @staticmethod
    async def is_liked(track, liked_tracks) -> bool:
        filtered_tracks: List[Track] = SpotifyTrack.track_difference([track], liked_tracks)
        return len(filtered_tracks) == 0
    

    @staticmethod
    async def get_radio(sp: SpotifyClient, track: str) -> List[Track]:
        data = {"track": track}
        radio_playlist = requests.post("http://localhost:8002/radio", json=data)
        radio_playlist_id = radio_playlist.json()["playlist"]
        playlist_tracks: List[Track] = await sp.playlist_tracks(radio_playlist_id, batch=True, chunk_size=1)
        return playlist_tracks
