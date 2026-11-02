# 🗳️ <img src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Great_Seal_of_the_United_States_%28obverse%29.svg" width="38" valign="middle" /> 2026 U.S. Midterm Elections: Real-Time Live Tracker 2026 U.S. Midterm Elections: Real-Time Live Tracker

A high-vibrancy, real-time analytics and tracking dashboard built with **Streamlit**, **Plotly**, and **Python** for the **2026 U.S. Midterm Elections**. Features live prediction market integration, a dynamic split-screen party tinting engine, Senate battleground watchlists, and live RSS news feeds.

![Streamlit App Status](https://img.shields.io/badge/Streamlit-App-orange?logo=streamlit)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Theme](https://img.shields.io/badge/Theme-Forced%20Light-yellow)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🚀 Key Features

* **High-Vibrancy Split-Screen Tints:** Features a dynamic background gradient that splits between Democratic Blue and Republican Red. The intensity and saturation scale automatically based on live win probabilities.
* **Confirmed Victory Banners:** Automatically triggers a flashing celebration banner complete with the U.S. Flag, the Great Seal of the United States, and bold declaration text when a chamber crosses the 99% win threshold.
* **Live Prediction Odds:** Connects to public live data feeds (Kalshi Elections API) for real-time contract pricing on House and Senate control.
* **Forced Light Theme Lock:** Configured via `.streamlit/config.toml` to permanently render in a clean, high-contrast light theme, bypassing system dark mode defaults.
* **Interactive Visualizations:** Stacked Plotly probability charts and detailed progress-tracked Senate battleground leaderboards (Ohio, Maine, Texas, Michigan, Alaska, Kansas, Iowa).
* **Live Breaking News Wire:** Pulls up-to-the-minute news coverage directly via the Google News RSS feed.

---

## 🛠️ Tech Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io/) (Locked to Light Mode)
* **Data Visualizations:** [Plotly Express](https://plotly.com/python/)
* **Data Processing:** Pandas, Requests
* **Live Feeds:** Kalshi Elections API, Google News RSS (`feedparser`)

---

## 📦 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/us-midterms-2026-tracker.git](https://github.com/YOUR-USERNAME/us-midterms-2026-tracker.git)
   cd us-midterms-2026-tracker
