import os
import requests

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["SPOTIFY_REFRESH_TOKEN"]

token = requests.post(
    "https://accounts.spotify.com/api/token",
    data={
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    },
    auth=(CLIENT_ID, CLIENT_SECRET),
).json()["access_token"]

response = requests.get(
    "https://api.spotify.com/v1/me/player/currently-playing",
    headers={
        "Authorization": f"Bearer {token}"
    },
)

if response.status_code == 200:
    data = response.json()
    song = data["item"]["name"]
    artist = data["item"]["artists"][0]["name"]
    text = f"🎧 Currently Playing\n\n**{song}** — {artist}"
else:
    text = "🎧 Currently Playing\n\nNothing right now"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start = "<!-- SPOTIFY:START -->"
end = "<!-- SPOTIFY:END -->"

before = readme.split(start)[0]
after = readme.split(end)[1]

new_readme = (
    before
    + start
    + "\n\n"
    + text
    + "\n\n"
    + end
    + after
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)
