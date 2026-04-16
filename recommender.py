import json
from ytmusicapi import YTMusic
import webbrowser
from mood_detector import _ask_groq

# Initialize YouTube Music API Client
ytmusic = YTMusic()

def get_recommendations_from_spotify(seed_track_id=None, target_features=None, mood_text=None, exclude_songs=None, limit=5):
    """
    Get track recommendations from Groq/Llama.
    Uses raw mood_text and exclude_songs to ensure fresh, relevant results.
    """
    exclude_str = ""
    if exclude_songs:
        exclude_str = f"\nCRITICAL: Do NOT recommend any of these songs you've already suggested: {', '.join(exclude_songs)}."

    if mood_text:
        prompt = f"""You are a world-class music curator. A user described their mood and music preference as:
"{mood_text}"

Based on this, recommend exactly {limit} songs.
RULES:
1. If the user specifies a language (like Hindi, Spanish, Punjabi, etc.), you MUST ONLY recommend songs in that language.
2. If no language is mentioned, default to popular global hits.
3. EXTREME VARIETY: Provide a fresh stack of songs. Do not repeat your typical go-to recommendations.{exclude_str}
4. Choose well-known, real songs.
"""

    elif seed_track_id:
        song_info = seed_track_id.replace("_", " ")
        prompt = f"""You are a world-class music curator. Recommend exactly {limit} songs that are 
highly similar in vibe and genre to '{song_info}'.
{exclude_str}
Choose popular, real songs. Prioritize variety and fresh picks."""

    elif target_features:
        prompt = f"""You are a world-class music curator. Recommend exactly {limit} popular songs matching 
these audio characteristics: {json.dumps(target_features)}. {exclude_str}"""
    else:
        return []
        
    prompt += """

Output ONLY a JSON array of objects. Each object must have:
- title: The exact song title
- artist: The primary artist name
- spotify_id: A unique ID string

Reply ONLY with valid JSON array. No markdown, no explanation."""
    
    text = _ask_groq(prompt)
    if not text:
        return []
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Recommendation parse error: {e}")
        return []

def get_ytmusic_video_id(title, artist):
    """
    Searches YouTube Music for the track and returns its video ID.
    """
    query = f"{title} {artist}"
    search_results = ytmusic.search(query, filter="songs", limit=1)
    
    if search_results:
        return search_results[0]['videoId']
    return None

def get_ytmusic_link(title, artist):
    """
    Searches YouTube Music for the track and returns its playable video URL.
    """
    video_id = get_ytmusic_video_id(title, artist)
    if video_id:
        return f"https://music.youtube.com/watch?v={video_id}"
    return None

def play_song_on_platform(url):
    """
    Opens the URL in the default web browser to start playback.
    """
    webbrowser.open(url)

def play_playlist_on_platform(video_ids):
    """
    Takes a list of YT Music video IDs and queues them into an anonymous playlist using youtube's watch_videos.
    """
    import requests
    if not video_ids: return
    
    # Generate an anonymous playlist on youtube
    url = f"https://www.youtube.com/watch_videos?video_ids={','.join(video_ids)}"
    try:
        response = requests.get(url, allow_redirects=True)
        # Convert the www.youtube.com playlist redirect into a music.youtube.com
        yt_music_url = response.url.replace("www.youtube.com", "music.youtube.com")
        webbrowser.open(yt_music_url)
    except Exception as e:
        print("Failed to generate playlist:", e)
