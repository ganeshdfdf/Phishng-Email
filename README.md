# Phishing Email Detector 🛡️📧

A modern, machine learning-powered web application designed to identify phishing attempts in email content. 

## 🌟 Overview

The **Phishing Email Detector** provides real-time security analysis for email messages. By utilizing a trained Random Forest model and heuristic feature extraction, it evaluates the probability of an email being a phishing attack.

### Key Features
- **Real-time ML Inference**: Instant classification using a Random Forest model.
- **Heuristic Analysis**: Detects suspicious keywords, URL patterns, and IP-based links.
- **Modern UI**: A responsive, interactive dashboard built with Streamlit.
- **Dual-Theme Support**: Fully optimized for both Light and Dark modes.
- **Security Insights**: Provides actionable tips and detailed vulnerability reports.

## 🏗️ Project Structure

```text
Phishng Email/
├── src/
│   ├── api/            # FastAPI Backend
│   │   └── main.py     # Inference API
│   ├── frontend/       # Streamlit UI
│   │   └── app.py      # Main UI file
│   ├── ml/             # Machine Learning pipeline
│   │   ├── train.py    # Synthetic data & training script
│   │   ├── features.py # Feature extraction logic
│   │   └── model.joblib # Trained model file
│   └── core/           # Shared core logic
├── data/               # Dataset storage (if any)
├── tests/              # Unit and integration tests
└── requirements.txt    # Project dependencies
```

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend API
Start the FastAPI server to handle analysis requests:
```bash
python src/api/main.py
```
*The API will be available at `http://localhost:8000`.*

### 4. Run the Frontend UI
In a separate terminal, launch the Streamlit dashboard:
```bash
streamlit run src/frontend/app.py
```
*The web interface will open at `http://localhost:8501`.*

## 🧠 Machine Learning Model

- **Engine**: Random Forest Classifier (`scikit-learn`)
- **Training Strategy**: Trained on a diverse set of synthetic phishing and legitimate ("ham") templates.
- **Features Extracted**:
  - `keyword_count`: Frequency of urgent or suspicious terms (e.g., "verify", "suspended").
  - `url_count`: Total number of links found in the text.
  - `ip_in_url`: Binary marker for URLs containing raw IP addresses (high phishing signal).
  - `email_length`: Overall length of the content.

## 🛡️ Security Tips
- Always check the sender's actual email address.
- Be wary of generic greetings (e.g., "Dear Valued Customer").
- Look for an artificial sense of urgency or threats.
- Hover over links to reveal the true destination.

## 🛠️ Built With
- **FastAPI** - High-performance backend API.
- **Streamlit** - Rapid UI development for data apps.
- **Scikit-learn** - Machine learning toolkit.
- **Joblib** - Model serialization.

---
*Created for proactive email security.*
