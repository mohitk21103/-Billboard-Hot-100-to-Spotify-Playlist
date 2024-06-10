import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "Add YOUR SPOTIFY CLIENT ID"
CLIENT_SECRET = "Add YOUR SPOTIFY CLIENT SECRET"


date = input("Which Year Do you want to travel to? Type the date in this format YYYY-MM-DD:")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(url=URL)
data = response.text
soup = BeautifulSoup(data, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

print(song_names)




sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Mohit Kanojiya",
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

