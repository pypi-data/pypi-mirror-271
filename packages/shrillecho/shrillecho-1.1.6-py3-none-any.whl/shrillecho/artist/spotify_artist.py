import asyncio
from datetime import datetime
import json
import math
import time
import requests
import spotipy
from shrillecho.spotify.client import SpotifyClient
from shrillecho.spotify.task_scheduler import TaskScheduler
from shrillecho.track.spotify_track import SpotifyTrack
from shrillecho.types.album_types import Album, ArtistAlbums, SeveralAlbums, SimplifiedAlbum, SimplifiedTrack
from shrillecho.types.artist_types import Artist, FollowerCount, SeveralArtists
from shrillecho.types.base_types import Followers
from shrillecho.types.track_types import SeveralTracks, Track
from shrillecho.user.user import SpotifyUserUtil
from shrillecho.utility.cache import cached
from shrillecho.utility.general_utility import get_id, is_earlier, sp_fetch
from typing import List



class SpotifyArtistUtil:

    @staticmethod
    def determine_main_artist(track: Track) -> Artist:
        """ The main artist is the artist who actually made the track, 
            so if its a remix , they are the creators of the remix but may not be listed
            as the first artist. The main artist does not include the feats just the core artist, 
            may extend to be feats..

            Args:
                track (Track): the track to determine the main artist of
        
            Returns:
                List[Artist]: list of artists in the playlist
        """

        main_artist = None

        if 'Remix' in track.name:
            for artist in track.artists:
                if artist.name in track.name:
                    main_artist = artist
            if not main_artist:
                main_artist = track.artists[0]
        else:
            main_artist = track.artists[0]

        return main_artist


    @staticmethod
    @cached(cache_key_prefix="followers", class_type=FollowerCount, expiry=3600)
    async def followers(sp: SpotifyClient, artist: str) -> int:
        """ the number of followers (ML form)

            Args:
                track (Artist): The artist to get the followers of (ML form)
        
            Returns:
                int: followers (ML form)
        """
        artist_id = get_id("artist", artist)
        data = {"artist": artist_id}
        followers_call = requests.post("http://localhost:8002/ml", json=data)
        followers = followers_call.json()
        return FollowerCount.from_json(json.dumps(followers))

    @staticmethod
    async def get_artist_track_ids(sp: SpotifyClient, artist_id) -> List[str]:
        """ Given an artist id, return all the associated track ids of that artist

            Args:
               sp (SpotifyClient): client
               artist_id (str): artist id (base64)
        
            Returns:
                int: followers (ML form)
        """
      
        artist_albums: List[SimplifiedAlbum] = await sp.artist_albums(artist=artist_id)
        
        task_scheduluer = TaskScheduler()

        tasks = [
            (sp.album_tracks, (album.id,)) for album in artist_albums
        ]
    
        task_scheduluer.load_tasks(tasks)

        
        album_tracks: List[SimplifiedTrack] = await task_scheduluer.execute_tasks(batch_size=20)
     
   
        track_ids = [item.id for item in album_tracks]

        return track_ids

    @staticmethod
    async def get_artist_tracks(sp: SpotifyClient, artist: str, unique: bool = True) -> List[Track]:
        """ Given an artist return all there tracks, unique is optional.

            Args:
               sp (SpotifyClient): client
               artist (str): artist id / uri / link
               unique: whether to remove duplicate tracks that appeared from the same release.
        
            Returns:
                int: followers (ML form)
        """
        
        artist_id = get_id("artist", artist)
        
        track_ids = await SpotifyArtistUtil.get_artist_track_ids(sp, artist_id)
     
        tracks: List[Track] = await SpotifyTrack.fetch_several_tracks(sp, track_ids)

        if unique:
            return set(tracks)
        
        return tracks
       
    
    @staticmethod
    async def get_artist_albums(sp: SpotifyClient, artist_id: str, simple=False) -> List[Album] | List[SimplifiedAlbum]:
        
        """ Given an artist id, return all albums """
        
        artist_albums: List[SimplifiedAlbum] = await sp.artist_albums(artist=artist_id)

        if simple:
            return artist_albums

        album_ids = [album.id for album in artist_albums]
        
        return SpotifyTrack.fetch_several_albums(sp, album_ids=album_ids)
    
    @staticmethod
    async def get_artist_new_releases(sp: SpotifyClient, artist_id: str, earliest_date: str ='2024-03-01' ) -> List[SimplifiedAlbum]:
       
        albums: List[SimplifiedAlbum] = []
        artist_albums: ArtistAlbums = await sp.artist_albums_single(artist=artist_id, offset=0)
        albums.extend(artist_albums.items)
        next = artist_albums.next
        
        while next != None:
           

            offset: int = artist_albums.offset + 50
            artist_albums: ArtistAlbums = await sp.artist_albums_single(artist=artist_id, offset=offset)

            if len(artist_albums.items) == 0:
                break

            last_album = artist_albums.items[-1]
            next = artist_albums.next

            if is_earlier(last_album.release_date, earliest_date):
                break

            albums.extend(artist_albums.items)

         
        return albums
    
    @staticmethod
    async def get_followed_new_releases(sp: SpotifyClient) -> List[SimplifiedAlbum]:
       
        followed_artists: List[Artist] = await SpotifyUserUtil.get_followed_artists(sp)
   

        ids = [artist.id for artist in followed_artists]

        task_scheduluer = TaskScheduler()

        tasks = [
            (SpotifyArtistUtil.get_artist_new_releases, (sp, artist_id,)) for artist_id in ids
        ]
    
        task_scheduluer.load_tasks(tasks)
   
        return await task_scheduluer.execute_tasks(batch_size=50)
     

    @staticmethod
    async def most_obscure_artists(sp: SpotifyClient, artist: str, artists: List[Artist], depth: int = 0) -> List[Artist]:
        
        if depth == 10:
            return artists

        artist_id = get_id("artist", artist)

        related_artists: List[Artist] = await sp.artist_related(artist=artist_id)
        
        most_obscure = math.inf
        most_obscure_artist = None

        for artist in related_artists:
            followers: FollowerCount = await SpotifyArtistUtil.followers(sp, artist=artist.id)
            follower_count = followers.followers

            if follower_count < most_obscure and artist not in artists:
                most_obscure = follower_count 
                most_obscure_artist = artist

        artists.append(most_obscure_artist)
        depth += 1

        return await SpotifyArtistUtil.most_obscure_artists(sp, most_obscure_artist.id, artists, depth)


    @staticmethod
    async def fetch_several_artists(sp: SpotifyClient, artist_ids: List[str]) -> List[Artist]:
        """ Fetch multiple artists

            Args:
                sp (SpotifyClient): client
                artist_ids (List[str]): list of ids to get the artist for
            
            Returns:
                List[Artist]: list of each artist
        """
        artists: List[Artist] = []
        for i in range(0, len(artist_ids), 50):
            chunk = artist_ids[i:i + 50]
            sev_artists: SeveralArtists = await sp.artists(chunk)
            artists.extend(sev_artists.artists)
        return artists

    @staticmethod
    async def get_playlist_artists(sp: SpotifyClient, playlist: str) -> List[Artist]:
        """ Given a playlist, returns all the artists on the playlist. Includes all artists of track and does not
            contain duplicate artists

            Args:
                sp (SpotifyClient): Spotify Client
                playlist (str): Playlist ID / URI / Link

            Returns:
                List[Artist]: list of artists in the playlist
        """

        playlist_id = get_id("playlist", playlist)

        playlist_tracks: List[Track] = await sp.playlist_tracks(playlist_id=playlist_id)

        artist_ids = set()

        for track in playlist_tracks:
            if track.artists and track.external_ids.isrc:
                for artist in track.artists:
                    artist_ids.add(artist.id)

        return SpotifyArtistUtil.fetch_several_artists(sp, list(artist_ids))
        


 

    