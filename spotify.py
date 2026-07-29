import os
import requests
import html

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["SPOTIFY_REFRESH_TOKEN"]

# Récupération du token
token_response = requests.post(
    "https://accounts.spotify.com/api/token",
    data={
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    },
    auth=(CLIENT_ID, CLIENT_SECRET),
)

token = token_response.json()["access_token"]

# Récupération de la musique
response = requests.get(
    "https://api.spotify.com/v1/me/player/currently-playing",
    headers={
        "Authorization": f"Bearer {token}"
    },
)

if response.status_code == 200 and response.json():
    data = response.json()

    track = data["item"]

    title = html.escape(track["name"])
    artist = html.escape(track["artists"][0]["name"])

    image = track["album"]["images"][0]["url"]

    progress = data["progress_ms"]
    duration = track["duration_ms"]

    percent = int(progress / duration * 100)

    status = "● LISTENING NOW"

else:
    title = "Nothing playing"
    artist = "Spotify"
    image = ""
    percent = 0
    status = "○ OFFLINE"


svg = f"""
<svg width="500" height="180" xmlns="http://www.w3.org/2000/svg">

<style>
.title {{
font: bold 18px Arial;
fill: white;
}}

.text {{
font: 14px Arial;
fill: #b3b3b3;
}}

.status {{
font: bold 12px Arial;
fill: #1DB954;
}}

.bar {{
animation: move 1s infinite;
}}

@keyframes move {{
0% {{ height: 10px; }}
50% {{ height: 30px; }}
100% {{ height: 10px; }}
}}
</style>


<rect width="500" height="180" rx="20" fill="#121212"/>


<text x="30" y="45" class="status">
{status}
</text>


<text x="30" y="80" class="title">
{title[:35]}
</text>


<text x="30" y="110" class="text">
{artist[:35]}
</text>


<rect x="30" y="135" width="260" height="8" rx="5" fill="#333"/>

<rect x="30" y="135" width="{260*percent/100}" height="8" rx="5" fill="#1DB954"/>


<rect class="bar" x="450" y="80" width="5" fill="#1DB954"/>
<rect class="bar" x="460" y="70" width="5" fill="#1DB954"/>
<rect class="bar" x="470" y="90" width="5" fill="#1DB954"/>


</svg>
"""


with open("spotify.svg", "w", encoding="utf-8") as f:
    f.write(svg)
