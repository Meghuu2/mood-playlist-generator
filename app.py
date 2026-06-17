"""
Mood Playlist Generator
------------------------
Takes a mood or activity description from the user, asks OpenAI to suggest
matching songs, finds those songs on Spotify, and creates a new playlist
in the user's account.
"""

import os
import json
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from openai import OpenAI

# Load API keys and config from .env
load_dotenv()

# Set up Spotify client (handles login/auth automatically)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private"
))

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def mood_to_songs(mood_text, num_songs=20):
    """Ask OpenAI to suggest real songs matching a mood or activity."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a music expert. Given a mood or activity "
                    f"description, suggest {num_songs} real, existing songs "
                    f"that fit well. Respond ONLY with JSON, no other text, "
                    f"in this exact format: "
                    f'{{"songs": [{{"title": "song title", "artist": "artist name"}}]}}'
                )
            },
            {"role": "user", "content": mood_text}
        ]
    )
    songs_json = response.choices[0].message.content
    return json.loads(songs_json)["songs"]


def search_tracks(songs):
    """Look up each AI-suggested song on Spotify and return matching track URIs."""
    track_uris = []
    for song in songs:
        query = f"track:{song['title']} artist:{song['artist']}"
        result = sp.search(q=query, type="track", limit=1)
        items = result["tracks"]["items"]
        if items:
            track_uris.append(items[0]["uri"])
    return track_uris


def create_playlist(mood_text, track_uris):
    """Create a new private playlist and add the found tracks to it."""
    playlist = sp.current_user_playlist_create(
        name=f"Mood: {mood_text}",
        public=False,
        description=f"Auto-generated playlist for: {mood_text}"
    )
    sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)
    return playlist["external_urls"]["spotify"]


if __name__ == "__main__":
    mood_text = input("How are you feeling, or what are you doing? ")

    print("Thinking of songs that match your mood...")
    songs = mood_to_songs(mood_text)

    print("Searching Spotify...")
    uris = search_tracks(songs)
    print(f"Found {len(uris)} tracks")

    link = create_playlist(mood_text, uris)
    print(f"Your playlist is ready: {link}")