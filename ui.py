import streamlit as st

def apply_custom_css():
    st.markdown(
        """
        <style>

        

        .stApp {
            background-color: #0b0f19;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }


        h1, h2, h3, h4, h5, h6 {
            color: #e0e0e0;
        }


        .header-banner {
            background: linear-gradient(90deg, #6b21a8, #c026d3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem;
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        .header-subtitle {
            color: #a8a2b5;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }


        div[data-testid="stFileUploader"] {
            border: 1px solid #3b2a54;
            border-radius: 12px;
            padding: 1.5rem;
            background-color: #141724;
            box-shadow: 0 4px 20px rgba(107, 33, 168, 0.15);
            transition: all 0.3s ease;
        }
        
        div[data-testid="stFileUploader"]:hover {
            border-color: #c026d3;
            box-shadow: 0 4px 25px rgba(192, 38, 211, 0.25);
        }


        div[data-testid="stChatInput"] {
            border: 1px solid #4a336e;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(107, 33, 168, 0.2);
            background-color: #1a1d2d;
        }
        

        div.stButton > button {
            background: linear-gradient(135deg, #7c3aed, #db2777);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(219, 39, 119, 0.3);
            color: white;
        }


        .insight-button div.stButton > button {
            background: #1f2335;
            border: 1px solid #3b2a54;
            color: #c084fc;
        }
        .insight-button div.stButton > button:hover {
            background: #2b234a;
            border-color: #d8b4fe;
            color: white;
            transform: none;
            box-shadow: none;
        }


        div[data-testid="stDataFrame"] {
            border: 1px solid #332145;
            border-radius: 10px;
            overflow: hidden;
            background-color: #10121c;
        }
        

        .streamlit-expanderHeader {
            background-color: #171926;
            border-radius: 8px;
            border: 1px solid #332145;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header():
    st.markdown('<h1 class="header-banner">DataYami 🔮</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Talk to your data instantly.</p>', unsafe_allow_html=True)
