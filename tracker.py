import asyncio
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def get_current_media_info():
    """
    Asynchronously fetches the currently playing media's title and artist from Windows.
    Returns:
        dict: {'title': str, 'artist': str} or None if nothing is playing/found.
    """
    try:
        sessions = await MediaManager.request_async()
        current_session = sessions.get_current_session()
        
        if current_session:
            info = await current_session.try_get_media_properties_async()
            return {
                "title": info.title,
                "artist": info.artist
            }
    except Exception as e:
        print(f"Error reading media info: {e}")
    return None

def get_now_playing():
    """
    Synchronous wrapper to get the currently playing media info.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        # If we are already running inside an event loop (e.g., inside Streamlit sometimes)
        # We can't use run_until_complete directly easily, but Streamlit is mostly sync
        # return None as a fallback or handle nested loops.
        # Use asyncio.run with a brand new thread if needed, but standard Streamlit allows run_until_complete here.
        # Let's try native run:
        return asyncio.run(get_current_media_info())
    else:
        return loop.run_until_complete(get_current_media_info())

if __name__ == "__main__":
    song = get_now_playing()
    print("Now Playing:", song)
