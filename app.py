import streamlit as st
import pandas as pd
from ui import apply_custom_css, render_header
from data_engine import query_data
from voice_input import process_voice_input


st.set_page_config(
    page_title="DataYami - Talk to your Data",
    page_icon="🔮",
    layout="wide"
)


apply_custom_css()


if "messages" not in st.session_state:
    st.session_state.messages = []


render_header()

@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        file.seek(0)
        df = pd.read_csv(file, encoding='latin1')
    return df


uploaded_file = st.file_uploader("Upload your CSV file here", type=["csv"])

if uploaded_file is not None:
    try:

        df = load_data(uploaded_file)
        
        with st.expander("Preview Data"):
            st.dataframe(df.head(10))
            
        st.markdown("---")
        

        st.markdown("### Quick Insights")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="insight-button">', unsafe_allow_html=True)
            if st.button("Dataset Overview"):
                st.session_state.messages.append({"role": "user", "content": "Give me a dataset overview"})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="insight-button">', unsafe_allow_html=True)
            if st.button("Check Missing Values"):
                st.session_state.messages.append({"role": "user", "content": "Show missing values"})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="insight-button">', unsafe_allow_html=True)
            if st.button("Show Data Types"):
                st.session_state.messages.append({"role": "user", "content": "What are the data types of the columns?"})
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        

        st.markdown("### Voice Input 🎙️")
        audio_value = st.audio_input("Speak your question")
        
        if audio_value:

            transcribed_text = process_voice_input(audio_value.getvalue())
            if transcribed_text:
                st.success(f"Transcribed: {transcribed_text}")

                st.session_state.messages.append({"role": "user", "content": transcribed_text})


        user_input = st.chat_input("Or type your question about the data here...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            

        st.markdown("### Conversation")
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    if message.get("type") == "plot":
                        st.plotly_chart(message["content"], use_container_width=True)
                    elif message.get("type") == "text":
                        st.write(message["content"])
                    elif message.get("type") == "both":
                        st.write(message["content"])
                        st.plotly_chart(message["figure"], use_container_width=True)
                        

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            user_query = st.session_state.messages[-1]["content"]
            with st.chat_message("assistant"):
                result = query_data(df, user_query)
                if result.get("error"):
                    st.error(result["error"])
                elif result.get("type") == "text":
                    st.write(result["content"])
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": result["content"]})
                elif result.get("type") == "plot":
                    st.plotly_chart(result["figure"], use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "type": "plot", "content": result["figure"]})
                elif result.get("type") == "both":
                    st.write(result["content"])
                    st.plotly_chart(result["figure"], use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "type": "both", "content": result["content"], "figure": result["figure"]})
                    
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")

else:
    st.info("👆 Please upload a CSV file to get started.")
