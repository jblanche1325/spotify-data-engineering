from pull_spotify import get_playlist_data
import pandas as pd

def extract_data(playlist_uri: str) -> pd.DataFrame:

    playlist_df = get_playlist_data(playlist_uri)

    return playlist_df

if __name__=='__main__':
    #extract_data("37i9dQZEVXbLRQDuF5jeBp")
    extract_data()