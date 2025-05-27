# audio_generator.py
from gtts import gTTS
import io
import streamlit as st # For error reporting

# @st.cache_data # Optional: Cache the TTS generation to avoid re-running for same text
def synthesize_text_gtts(text: str, language_code="en", slow=False) -> bytes | None:
    """
    Synthesizes speech from the input string of text using gTTS.

    Args:
        text: The text to synthesize.
        language_code: The language code (e.g., "en", "fr", "es").
                       See gTTS documentation for supported languages.
        slow: Whether to read text slowly.

    Returns:
        The raw audio bytes (MP3 format) if successful, otherwise None.
    """
    if not text or not text.strip():
        st.error("Input text cannot be empty.")
        return None

    try:
        print(f"Requesting gTTS for text: {text[:100]}...") # Log request

        # Create gTTS object
        tts = gTTS(text=text, lang=language_code, slow=slow)

        # Save the synthesized speech to a bytes buffer
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0) # Rewind the buffer to the beginning
        audio_bytes = mp3_fp.read()

        print("gTTS synthesis successful.")
        return audio_bytes

    except Exception as e:
        # gTTS errors can be less specific than Cloud API errors
        st.error(f"❌ Error during gTTS synthesis: {e}")
        st.error("Ensure you have an active internet connection. The gTTS service might be temporarily unavailable or the language code might be invalid.")
        print(f"❌ gTTS Error: {e}") # Log detailed error
        return None