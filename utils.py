import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass
            
    if not api_key:
        st.error("GROQ_API_KEY is not set. Please add it to your .env file or Streamlit secrets.")
        st.stop()
        
    return ChatGroq(
        model_name="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.0
    )
