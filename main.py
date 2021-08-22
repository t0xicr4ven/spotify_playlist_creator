import os
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOT_ID = os.environ.get('spot_ID')
SPOT_SECRET = os.environ.get('spot_secret')
REDIR_URL = "http://example.com"
# auth with spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOT_ID,
        client_secret=SPOT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.me()['id']


BASE_URL = "https://www.billboard.com/charts/hot-100/"
year = input("""Which year do you want to travel to? Enter the date in this format YYYY-MM-DD: """) 
# get top 100 from selected year
response = requests.get(url=f"{BASE_URL}{year}")
soup = BeautifulSoup(response.text, 'html.parser')
song_names = [song.getText() for song in soup.find_all('span',
    class_="chart-element__information__song text--truncate color--primary")]
artist_names = [artist.getText() for artist in soup.find_all('span', class_="chart-element__information__artist text--truncate color--secondary")]

#Searching Spotify for songs by title
song_uris = []
fixed_year = year.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{fixed_year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100",
        public=False)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


