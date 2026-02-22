from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import sys
import numpy as np

# Add project root to sys.path to allow imports from src
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.ml.features import FeatureExtractor

app = FastAPI(title="Phishing Email Detection API")

model = None
feature_extractor = None
# Define feature order to match training
FEATURE_ORDER = ['keyword_count', 'url_count', 'ip_in_url', 'email_length']

class EmailRequest(BaseModel):
    content: str

class PredictionResponse(BaseModel):
    is_phishing: bool
    confidence: float
    features: dict

@app.on_event("startup")
def load_model():
    global model, feature_extractor
    # Path relative to this file: ../ml/model.joblib
    model_path = os.path.join(os.path.dirname(__file__), '../ml/model.joblib')
    if not os.path.exists(model_path):
        # Fallback or wait? For now, we expect it to exist.
        print(f"Warning: Model not found at {model_path}. API will fail to predict.")
    else:
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
    
    feature_extractor = FeatureExtractor()

@app.post("/predict", response_model=PredictionResponse)
def predict(email: EmailRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded or found")
    
    # Extract features
    features = feature_extractor.extract_features(email.content)
    
    # Prepare vector
    feature_vector = [features[name] for name in FEATURE_ORDER]
    
    # Reshape for single sample (1, n_features)
    feature_vector = np.array(feature_vector).reshape(1, -1)
    
    # Predict
    prediction = model.predict(feature_vector)[0]
    probabilities = model.predict_proba(feature_vector)[0]
    
    # 1 is Phishing, 0 is Safe
    is_phishing = bool(prediction == 1)
    confidence = float(probabilities[1]) if is_phishing else float(probabilities[0])
    
    return {
        "is_phishing": is_phishing,
        "confidence": round(confidence, 4),
        "features": features
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
