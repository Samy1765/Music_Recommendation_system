import streamlit as st
from ui_utils import apply_custom_css
from mood_detector import analyze_mood_text
from recommender import get_recommendations_from_spotify, get_ytmusic_link, play_song_on_platform, play_playlist_on_platform, get_ytmusic_video_id

st.set_page_config(page_title="Mood Studio | SonicMood", layout="wide", page_icon="📝")
apply_custom_css()

# Register session state
if "history" not in st.session_state:
    st.session_state.history = []
if "seen_songs" not in st.session_state:
    st.session_state.seen_songs = set()

st.title("💬 Mood Studio")
st.markdown("<p style='text-align: center; color: #a0aec0; margin-top: -20px; margin-bottom: 40px;'>Describe your vibe, and the AI DJ will handle the rest.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### How are you feeling?")
    user_mood = st.text_area("Describe your mood here:", placeholder="E.g., I'm feeling extremely exhausted but hopeful today.", height=150)
    
    if st.button("Generate Soundscape", type="primary"):
        if user_mood:
            with st.spinner("AI DJ is analyzing your vibe..."):
                targets = analyze_mood_text(user_mood)
                
            if targets:
                st.session_state.targets_col2 = targets
                st.session_state.mood_text_col2 = user_mood
                with st.spinner("Curating the perfect playlist..."):
                    # Pass the seen songs to exclude them
                    new_recs = get_recommendations_from_spotify(
                        mood_text=user_mood, 
                        exclude_songs=list(st.session_state.seen_songs),
                        limit=5
                    )
                    st.session_state.recs_col2 = new_recs
                    # Track these songs so we don't see them again next time
                    for r in new_recs:
                        st.session_state.seen_songs.add(f"{r['title']} by {r['artist']}")
            else:
                st.error("Failed to parse mood.")
        else:
            st.warning("Please enter a mood description.")

# Render recommendations
if "recs_col2" in st.session_state and st.session_state.recs_col2:
    with col2:
        st.markdown("### Your Custom Mix")
        for r in st.session_state.recs_col2:
            st.markdown(f'''
            <div class="track-card">
                <p class="track-title">{r['title']}</p>
                <p class="track-artist">{r['artist']}</p>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button(f"Play Track", key=f"auto_{r['spotify_id']}", type="secondary"):
                yt_url = get_ytmusic_link(r['title'], r['artist'])
                if yt_url:
                    # Log event
                    st.session_state.history.append({"type": "Song Played", "title": r['title'], "artist": r['artist']})
                    play_song_on_platform(yt_url)
                    st.success("Enjoy the music!")
                    
        st.write("---")
        if st.button("▶️ Play All as YT Music Playlist", type="primary", key="playlist_col2"):
            with st.spinner("Building custom playlist..."):
                vids = [get_ytmusic_video_id(r['title'], r['artist']) for r in st.session_state.recs_col2]
                valid_vids = [v for v in vids if v]
                
                # Log event
                st.session_state.history.append({"type": "Playlist Generated", "title": "Mood Studio Custom Mix", "artist": f"{len(valid_vids)} Tracks"})
                
                play_playlist_on_platform(valid_vids)
                st.success("Custom playlist launched!")

        with st.expander("Show AI Target Profile Data"):
            st.json(st.session_state.targets_col2)
