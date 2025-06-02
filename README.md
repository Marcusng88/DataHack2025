# 🧬 DataHacks2025 – AI-Powered EDA & Chat Assistant

Welcome to **DataHacks2025**, a smart data exploration app built for the DataHack 2025 hackathon! This app combines interactive dashboards with powerful AI agents using **Google ADK** and **LlamaIndex**, enabling deep insights and natural language understanding of the dataset about SDG 14 -Lfe Under Water.

---

## 🌟 Features

### 📊 1. General EDA Dashboard
- Explore the dataset as a whole
- Summary statistics and distribution analysis

### 🐾 2. Species-Specific Dashboard + Gemini Insights
- Select a species from the dropdown
- View EDA specific to that species
- Get intelligent, insights generated via **Google ADK** using EDA that is done by us 

### 💬 3. LlamaIndex Chat Assistant
- Conversational interface using LlamaIndex
- Asynchronous agent runner with context memory
- Ask data-related or general queries in natural language

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/DataHacks2025.git
cd DataHacks2025
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 API Configuration

This app uses the **Google Gemini API** for insights and natural language processing.

### Steps:

1. Copy the example environment file:

```bash
cp .env-example .env    # Windows: copy .env-example .env
```

2. Paste your Google API key in \`.env\`:

```env
GOOGLE_API_KEY=your-google-api-key-here
```

> 🔑 Get your API key from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

---

## ▶️ Running the App

```bash
streamlit run main.py
```

Open the URL shown in your terminal (usually \`http://localhost:8501\`) to start using the app.

---


## 🛠 Tech Stack

- **Python** 🐍
- **Streamlit** – for dashboards and UI
- **LlamaIndex** – for conversational agent
- **Google ADK** – to access Gemini models
- **Pandas, NumPy** – for data processing
- **Matplotlib, Seaborn, Plotly** – for visualization

---

## 📌 Notes

- All dashboards run fully locally (except Gemini and LlamaIndex API calls).
- API usage is subject to quota limits — monitor your usage in Google AI Studio.
- This app uses in-memory session and artifact services; ideal for demo/prototype use.


---

## 🙏 Acknowledgements

- [Google AI Studio](https://makersuite.google.com/) for the Gemini API
- [LlamaIndex](https://www.llamaindex.ai/) for the powerful agent framework
- [Streamlit](https://streamlit.io/) for rapid UI development


