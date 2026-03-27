# DataYami 🔮 - Talk to Your Data

DataYami ("Antaryami" – the one who knows everything) is a modern, voice-enabled conversational AI agent for chatting with your CSV data. It leverages Streamlit, Pandas, Plotly, and the powerful Groq Llama-3 70B model to instantly analyze datasets, generate visual insights, and return numerical summaries.

## ✨ Features
* **Conversational Analytics:** Ask questions about your CSV in plain English.
* **Voice Input:** Use the built-in browser microphone to simply speak your questions! (Powered by Groq Whisper)
* **Instant Visualizations:** Generate Plotly charts on the fly.
* **Beautiful Modern UI:** Deep purple and black aesthetics with elegant glow effects.
* **Quick Insights:** One-click buttons to get dataset overviews, missing values, and data types.

## 🛠️ Tech Stack
* **Frontend:** Streamlit, Custom CSS
* **Data Processing:** Pandas
* **Visualization:** Plotly
* **AI / Intelligence:** Langchain, Groq (Llama-3.3-70b-versatile for text/code, Whisper for audio)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Chat-with-csv
   ```

2. **Install Dependencies:**
   Ensure you have Python 3.9+ installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Groq API Key:**
   Get a free API key from [Groq](https://console.groq.com/). Set it in your environment:
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```
   *Alternatively, add it to `.streamlit/secrets.toml`.*

## 🏃 Running the App

Run the application locally with Streamlit:
```bash
streamlit run app.py
```

## 📊 Example Questions
Once you upload the included `sample.csv` or your own data, try asking:
- "What is the total sales amount?"
- "Plot a bar chart showing Sales per Region."
- "Show me the top 3 products by Profit."
- "Which region sold the most Quantity?"

## 🏗️ Architecture
- `app.py`: Main Streamlit application and layout structure.
- `ui.py`: Manages styling, theming, and headers.
- `data_engine.py`: Handles secure code generation and execution via LLM to parse data frames safely.
- `voice_input.py`: Routes audio input to Groq's Whisper API for fast transcription.

## 🔮 Future Improvements
* Multi-CSV support (joining tables dynamically).
* Exporting generated charts as PNG/PDF.
* Advanced statistical modeling (regression, forecasting).

---
*Built with ❤️ utilizing the lightning-fast Groq inference endpoints.*
