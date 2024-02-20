
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

    def spotify_credentials(self) -> spotipy:
        spotify_key = os.getenv('SPOTIFY_KEY')
        spotify_secret = os.getenv('SPOTIFY_SECRET')

        client_credentials_manager = SpotifyClientCredentials(client_id=spotify_key, 
                                                    client_secret=spotify_secret)

        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        return sp
    
    def get_playlist_data(self, playlist_uri: str) -> pd.DataFrame:

        '''Create a DataFrame for a Spotify playlist

        This function pulls song and artist info from each song 
        on the given playlist

        Args:
            playlist_uri (str): The playlist_uri to pull info from

        Returns:
            DataFrame of playlist data
        '''
        sp = self.spotify_credentials()

        tracks = []

        #playlist_uri = '37i9dQZEVXbLRQDuF5jeBp'
        playlist = sp.playlist_tracks(playlist_uri)["items"]

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
            # Album Name
            track_album_name = track['track']['album']['name']
            # Album URI
            track_album_uri = track['track']['album']['uri']

            # Append results to list
            tracks.append([track_id, track_uri, track_name, track_artists, track_popularity, track_explicit, track_duration_ms, track_album_name, track_album_uri])

            # Tracks DataFrame
            tracks_df_cols = ['track_id', 'track_uri', 'track_name', 'track_artists', 'track_popularity', 'track_explicit', 'track_duration_ms', 'track_album_name', 'track_album_uri']
            tracks_df = pd.DataFrame(tracks, columns=tracks_df_cols)

            # Pull track URIs to retrieve audio data
            all_track_uris = tracks_df['track_uri'].to_list()

            # Initiate audio features list
            audio_features = []
            # Loop through each track and pull audio features
            for track_uri in all_track_uris[0:4]:
                feat = sp.audio_features(track_uri)[0]
                track_acousticness = feat['acousticness']
                track_danceability = feat['danceability']
                track_energy = feat['energy']
                track_speechiness = feat['speechiness']
                track_instrumentalness = feat['instrumentalness']
                track_loudness = feat['loudness']
                track_tempo = feat['tempo']
                track_liveness = feat['liveness']
                track_valence = feat['valence']

                analysis = sp.audio_analysis(track_uri)['track']
                track_time_signature = analysis['time_signature']
                track_key = analysis['key']

                # Append results to list
                audio_features.append([track_uri, track_acousticness, track_danceability, track_energy, track_speechiness, track_instrumentalness, track_loudness, track_tempo, track_liveness, track_valence, track_time_signature, track_key])

                # Features DataFrame
                features_df_cols = ['track_uri', 'track_acousticness', 'track_danceability', 'track_energy', 'track_speechiness', 'track_instrumentalness', 'track_loudness', 'track_tempo', 'track_liveness', 'track_valence', 'track_time_signature', 'track_key']
                features_df = pd.DataFrame(audio_features, columns=features_df_cols)

            # Join track_df and feature_df
            playlist_df = tracks_df.merge(features_df, how='inner', on='track_uri')
        
        return playlist_df