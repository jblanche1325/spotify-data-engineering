
import os

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dataclasses import dataclass

@dataclass
class DataExtractionConfig:
    raw_data_path: str=os.path.join('data', 'raw', 'raw.csv')

class ExtractData:
    def __init__(self):
        self.extraction_config = DataExtractionConfig()

    def spotify_credentials(self) -> Spotify:
        spotify_key = os.getenv('SPOTIFY_KEY')
        spotify_secret = os.getenv('SPOTIFY_SECRET')

        client_credentials_manager = SpotifyClientCredentials(client_id=spotify_key, 
                                                    client_secret=spotify_secret)

        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        return sp
    
    def get_top_50_playlist_tracks(self, playlist: dict) -> pd.DataFrame:

        sp = spotify_credentials()

        tracks = []

        top_50_us_playlist_uri = '37i9dQZEVXbLRQDuF5jeBp'
        playlist = sp.playlist_tracks(top_50_us_playlist_uri)["items"]

        for track in playlist:

            # Track ID
            track_id = track['track']['id']
            # Track URI
            track_uri = track['track']['uri']
            # Track Name
            track_name = track['track']['name']
            # Artist Info
            artists = track['track']['artists']
            track_artists = []
            #track_artist_id = []
            for artist in artists:
                artist_name = artist['name']
                artist_id = artist['id']
                track_artists.append([artist_name, artist_id])
            # Track Popularity
            track_popularity = track['track']['popularity']
            # Is Track Explicit
            track_explicit = track['track']['explicit']
            # Track Duration (ms)
            track_duration_ms  = track['track']['duration_ms']

            # Append results to list
            tracks.append([track_id, track_uri, track_name, track_artists, track_popularity, track_explicit, track_duration_ms])

            # Tracks DataFrame
            tracks_df_cols = ['track_id', 'track_uri', 'track_name', 'track_artists', 'track_popularity', 'track_explicit', 'track_duration_ms']
            tracks_df = pd.DataFrame(tracks, columns=tracks_df_cols)

        return tracks_df, 