# Mood Playlist Generator

A command-line tool that turns a mood or activity description into a real Spotify playlist. Type how you're feeling, and it builds a 20-track playlist for you, fully automatically.

## How it works

1. You describe your mood or activity in plain English (e.g. "tired but need to focus", "pumped for the gym")
2. OpenAI's API interprets that description and suggests real songs that fit
3. The Spotify Web API searches for those songs and finds exact matches
4. A new playlist is created in your Spotify account and populated with the matched tracks

## Example

How are you feeling, or what are you doing? rainy day, need to focus
Thinking of songs that match your mood...
Searching Spotify...
Found 18 tracks
Your playlist is ready: https://open.spotify.com/playlist/...

## Technologies used

- Python 3
- Spotify Web API (via the spotipy library) - OAuth authentication, track search, playlist creation
- OpenAI API (gpt-4o-mini) - mood-to-song interpretation
- python-dotenv - secure handling of API credentials

## Setup

1. Clone this repository
2. Install dependencies:
   pip install spotipy python-dotenv openai
3. Create a Spotify Developer app at developer.spotify.com with redirect URI http://127.0.0.1:8888/callback
4. Create an OpenAI API key at platform.openai.com
5. Create a .env file in the project root with:
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
   OPENAI_API_KEY=your_openai_key
6. Run the script:
   python3 app.py

## Notes

This project was built against Spotify's Web API following their February 2026 platform changes, which removed several legacy endpoints (including the original recommendations endpoint) for newly created developer apps. As a result, the playlist generation logic uses AI-suggested songs matched via Spotify's search endpoint, rather than Spotify's native audio-feature-based recommendation engine.

## Known issue: playlist links sometimes fail to open

The script prints a working open.spotify.com link for the created playlist. Verified server-side, the playlist and link are valid and load correctly when fetched directly. However, some users may see a generic "Something went wrong" error when clicking the link from certain browsers or devices. This is a known, widely-reported client-side bug on Spotify's end (unrelated to this project), affecting playlist loading sporadically across web, mobile, and desktop clients. If you hit it, search for the playlist by name directly inside the Spotify app instead, it will be there.