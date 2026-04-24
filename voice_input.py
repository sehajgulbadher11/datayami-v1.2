import os
import streamlit as st
from groq import Groq
import io
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass
            
    if not api_key:
        st.error("GROQ_API_KEY is not set. Please add it to your .env file or Streamlit secrets.")
        st.stop()
        
    return Groq(api_key=api_key)

def process_voice_input(audio_bytes):

    client = get_groq_client()
    
    with st.spinner("Transcribing audio..."):
        try:

            audio_file = ("audio.wav", audio_bytes, "audio/wav")
            
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                prompt="The user is asking a question about a dataset.",
                response_format="json",
                language="en",
                temperature=0.0
            )
            

            text = transcription.text.strip()

            text = text.replace("?", "").replace(".", "")
            
            return text
        except Exception as e:
            st.error(f"Error during voice transcription: {e}")
            return None
