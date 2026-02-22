import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import sys

# Ensure src is in path if running directly
# This assumes the script is located at src/ml/train.py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.ml.features import FeatureExtractor
from src.ml.preprocessing import clean_text

def generate_synthetic_data(n_samples=200):
    """
    Generates synthetic phishing and ham emails for training.
    """
    data = []
    
    # Phishing templates
    phishing_templates = [
        "Urgent: Verify your account immediately at {url}",
        "Your account has been suspended. Click here to restore access: {url}",
        "Confirm your password to avoid service interruption. {url}",
        "We noticed unusual activity on your bank account. Login here: {url}",
        "Security Alert: Someone tried to access your account from {ip}. Verify now: {url}",
        "Win a free iPhone! Claim yours at {url}",
        "Your package is pending delivery. Update address here: {url}"
    ]
    
    # Ham templates
    ham_templates = [
        "Meeting at 3 PM regarding the project updates.",
        "Can you send over the report by EOD?",
        "Lunch plans for tomorrow? Let me know.",
        "Attached is the invoice for last month's services.",
        "Happy Birthday! Hope you have a great day.",
        "The server will be down for maintenance tonight.",
        "Please review the attached document.",
        "Let's catch up next week."
    ]
    
    phishing_urls = [
        "http://secure-login-update.com",
        "http://verify-account-now.net/login",
        "http://192.168.1.1/update",
        "http://paypal-secure-check.com",
        "http://bank-of-america-security.com",
        "http://apple-support-id.com",
        "http://dhl-tracking-update.net"
    ]
    
    ham_urls = [ # Some ham emails might have URLs too
        "http://google.com",
        "https://www.linkedin.com",
        "http://company-portal.internal",
        "https://github.com",
        "https://stackoverflow.com",
        "https://docs.python.org",
        "https://en.wikipedia.org"
    ]
    
    import random
    
    for _ in range(n_samples // 2):
        # Phishing
        template = random.choice(phishing_templates)
        url = random.choice(phishing_urls)
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        # Randomly choose if ip is used or not
        text = template.format(url=url, ip=ip)
        data.append({"text": text, "label": 1}) # 1 for Phishing
        
        # Ham
        template = random.choice(ham_templates)
        # Occasionally add a safe URL to ham
        if random.random() < 0.3:
            text = template + " Check this: " + random.choice(ham_urls)
        else:
            text = template
        data.append({"text": text, "label": 0}) # 0 for Ham
        
    return pd.DataFrame(data)

def train_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data(n_samples=500)
    
    print("Extracting features...")
    extractor = FeatureExtractor()
    
    features_list = []
    # Use clean_text before extracting features?
    # features.py methods seem to handle raw text (e.g. url extraction)
    # clean_text removes special characters which might remove URLs!
    # Let's check preprocessing.py again.
    # It removes punctuation, HTML tags. It DOES convert to lowercase.
    # FeatureExtractor looks for 'http' in extract_features.
    # If clean_text removes ':', 'http://' becomes 'http//' or similar if punctuation is removed.
    # preprocessing.py line 21: text.translate(str.maketrans('', '', string.punctuation)) -> removes ':' and '/' and '.'
    # This will BREAK URL extraction.
    
    # DECISION: FeatureExtractor should work on RAW text for URL features.
    # However, keyword matching might benefit from lowered text.
    # The FeatureExtractor class does `keyword in email_text.lower()` so it handles casing.
    
    # I will pass raw text to extractor.
    
    for text in df['text']:
        # cleaned = clean_text(text) # Skip aggressive cleaning that removes URL structures
        features = extractor.extract_features(text)
        features_list.append(features)
        
    X = pd.DataFrame(features_list)
    y = df['label']
    
    print(f"Features shape: {X.shape}")
    print(f"Feature names: {X.columns.tolist()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    print("Training RandomForest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
