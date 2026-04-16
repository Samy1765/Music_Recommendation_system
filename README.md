# 🎧 Music Recommendation System

Welcome to the **Music Recommendation System**, a practical tool that tracks your listening habits and suggests new music based on the mood and style of what you're currently playing.

## 🌟 Features

- **🎙️ Live Audio Sync:** Tracks what's playing in real-time on your system (Windows Media).
- **📡 Audio Feature Estimation:** Uses AI to estimate musical features like *Valence* (positivity), *Energy*, *Danceability*, and *Acousticness*.
- **🧠 Mood Analysis:** Categorizes your current music vibe (e.g., "Relaxed & Chill", "Angry & Tense").
- **✨ Smart Recommendations:** Generates song suggestions that match your current listening profile and plays them on YouTube Music.
- **🎨 Visual Insights:** Displays an interactive Radar Chart to visualize your music's characteristics.

---

## 📖 The Backstory: Switching to Groq

Originally, this project relied on the **Spotify API** and **Google/YouTube APIs**. However, due to restrictive policies and credit issues with those services, we switched to **Groq (Llama 3.3)**. 

By using an AI model to analyze track features and generate recommendations, the system is more flexible, avoids expensive API paywalls, and works dynamically without needing a pre-built database for every song.

---

## 🛠️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Samy1765/Music_Recommendation_system.git
cd Music_Recommendation_system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your Environment
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🔑 How to get your Groq API Key

To get your API key for the analysis engine:

1.  Visit the [**Groq Cloud Console**](https://console.groq.com/).
2.  Sign up or log in.
3.  Go to the **API Keys** section.
4.  Create a new API key and copy it to your `.env` file.

---

## 🚀 Running the App

Launch the application using Streamlit:

```bash
streamlit run app.py
```

Play a song on your computer and click **SYNC AUDIO SOURCE** in the dashboard to start the analysis!
