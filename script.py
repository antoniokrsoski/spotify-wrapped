import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
from datetime import date
import gspread

# Spotify API credentials
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback/'
scope = 'user-top-read'

# Spotify API authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=redirect_uri, 
    scope=scope
    ))

# Get top tracks

# Get track ids
def get_track_ids(top_tracks):
    track_ids = []
    for item in top_tracks['items']:
        track_ids.append(item['id'])
    return track_ids

def get_track_features(track_id):
    meta = sp.track(track_id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotipy_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotipy_url, album_cover]
    return track_info

def insert_to_gsheet(track_ids, time_period):
    # loop over track ids 
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.2)
        track = get_track_features(track_ids[i])
        tracks.append(track)
    
    # create dataset
    df = pd.DataFrame(tracks, columns = ["name", "album", "artist", "spotify_url", "album_cover"])
    
    # insert into google sheet
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open("wrapped")
    worksheet = sh.worksheet(f"{time_period}")
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print("Done")

time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    track_ids = get_track_ids(top_tracks)
    insert_to_gsheet(track_ids, time_period)



