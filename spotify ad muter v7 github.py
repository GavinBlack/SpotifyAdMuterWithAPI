import time
import pyaudio
import pycaw.pycaw as audio
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import requests.exceptions

# Replace with your own Spotify API credentials
client_id = 'client id here'
client_secret = 'client secret here'
redirect_uri = 'http://localhost:8888/callback'

# Set up authentication and get the current user's ID
scope = 'user-read-playback-state,user-modify-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))
user_id = sp.current_user()['id']

# Get the default audio device
p = pyaudio.PyAudio()
devices = p.get_device_info_by_host_api_device_index(0, 0)
default_device = devices["name"].encode()

# Start muting/unmuting ads
while True:
    try:
        current_track = sp.current_playback()
        if current_track['currently_playing_type'] == 'ad':
            # Set the mute state to True
            sessions = audio.AudioUtilities.GetAllSessions()
            for session in sessions:
                if session.Process and session.Process.name() == "Spotify.exe":
                    volume = session.SimpleAudioVolume
                    volume.SetMute(1, None)
        else:
            # Set the mute state to False
            sessions = audio.AudioUtilities.GetAllSessions()
            for session in sessions:
                if session.Process and session.Process.name() == "Spotify.exe":
                    volume = session.SimpleAudioVolume
                    volume.SetMute(0, None)
        time.sleep(1)
    except:
        # Ignore any exceptions and continue looping
        pass

    time.sleep(1)
