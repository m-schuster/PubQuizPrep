import spotipy
from spotipy.oauth2 import SpotifyOAuth
import qrcode
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

SCOPE = 'playlist-modify-public'
CACHE_PATH = '.spotify_cache'

def create_spotify_playlist(songs_dict, topic):
    auth_manager = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                client_secret=SPOTIFY_CLIENT_SECRET,
                                redirect_uri=SPOTIFY_REDIRECT_URI,
                                scope=SCOPE,
                                cache_path=CACHE_PATH)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_id = sp.current_user()['id']
    playlist_name = f"Pub Quiz Playlist: {topic}"
    playlist_description = "An automatically created playlist for a pub quiz."
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)
    playlist_id = playlist['id']

    # Add tracks to playlist
    track_ids = []
    for artist, song in songs_dict.items():
        query = f"artist:{artist} track:{song}"
        result = sp.search(q=query, type='track', limit=1)
        if result['tracks']['items']:
            track_id = result['tracks']['items'][0]['id']
            track_ids.append(track_id)

    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids)
        print(f"{len(track_ids)} Songs konnten der Spotify Playlist hinzugefügt werden!")
        
    # Generate the QR code
    playlist_url = playlist['external_urls']['spotify']
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(playlist_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_path = "resources/temp/playlist_qr_code.png"
    img.save(img_path)

    return playlist_url, img_path