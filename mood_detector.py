import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

# Initialize Groq Client
try:
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print(f"Groq Init Error: {e}")
    groq_client = None

GROQ_MODEL = "llama-3.3-70b-versatile"

def _ask_groq(prompt):
    """
    Internal helper to send a prompt to Groq and return the raw text response.
    """
    if not groq_client:
        return None
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.2,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq API error: {e}")
        return None

def get_track_audio_features(song_title, artist_name):
    """
    Uses Groq (Llama 3) to estimate a track's valence, energy, danceability, and acousticness.
    """
    prompt = f"""Estimate the musical audio features for the song '{song_title}' by {artist_name}.
Output a JSON object with the following keys (all values should be floats between 0.0 and 1.0):
- valence: (0.0 = sad/angry/depressed, 1.0 = happy/euphoric/cheerful)
- energy: (0.0 = calm/relaxed, 1.0 = intense/fast/noisy)
- danceability: (0.0 = not danceable, 1.0 = highly danceable)
- acousticness: (0.0 = electronic, 1.0 = acoustic)

Reply ONLY with valid JSON. Do not include markdown formatting like ```json."""

    text = _ask_groq(prompt)
    if not text:
        return None
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        data['track_id'] = f"{song_title}_{artist_name}".replace(" ", "_")
        return data
    except Exception as e:
        print(f"Failed to parse Groq response: {e}")
        return None

def analyze_mood_text(mood_text):
    """
    Uses Groq (Llama 3) to translate a user's text mood into audio feature targets.
    """
    prompt = f"""The user has described their current mood as: "{mood_text}".

Translate this mood into target audio metrics and identify any specific language or genre preferences mentioned.
Output a JSON object with the following keys (all values should be floats between 0.0 and 1.0 where applicable):
- target_valence: (0.0 = sad, 1.0 = happy)
- target_energy: (0.0 = calm, 1.0 = intense)
- target_danceability: (0.0 = not danceable, 1.0 = highly danceable)
- target_acousticness: (0.0 = electronic, 1.0 = acoustic)
- preferred_language: (e.g., "Hindi", "English", "Spanish", or null if not specified)
- preferred_genre: (e.g., "Bollywood", "Lo-fi", "Rock", or null if not specified)

Reply ONLY with valid JSON. Do not include markdown formatting like ```json."""

    text = _ask_groq(prompt)
    if not text:
        return None
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Failed to parse Groq response: {e}")
        return None

def interpret_mood_from_features(valence, energy):
    """
    Simple quadrant interpretation of valence and energy.
    """
    if valence >= 0.5 and energy >= 0.5:
        return "Happy & Excited"
    elif valence >= 0.5 and energy < 0.5:
        return "Relaxed & Chill"
    elif valence < 0.5 and energy >= 0.5:
        return "Angry & Tense"
    else:
        return "Sad & Depressed"


