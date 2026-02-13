from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import xgboost as xgb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent   
MODELS_DIR = BASE_DIR / "models"

app = FastAPI(title="Phishing Detection API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_url = xgb.XGBClassifier()
model_url.load_model(str(MODELS_DIR / "xgboost_model.json"))

vectorizer = joblib.load(str(MODELS_DIR / "tfidf_vectorizer.pkl"))

model_text = xgb.XGBClassifier()
model_text.load_model(str(MODELS_DIR / "xgboost_text_model.json"))

meta_model = joblib.load(str(MODELS_DIR / "meta_learner.pkl"))

class PredictionRequest(BaseModel):
    url_features: list
    email_text: str = ""

@app.post("/predict")
def predict(req: PredictionRequest):
    features = np.array(req.url_features).reshape(1, -1)
    p_url = model_url.predict_proba(features)[0, 1]
    
    if req.email_text.strip():
        X_text = vectorizer.transform([req.email_text])
        p_text = model_text.predict_proba(X_text)[0, 1]
    else:
        p_text = 0.5
    
    meta_input = np.array([[p_url, p_text]])
    prob = meta_model.predict_proba(meta_input)[0, 1]
    
    return {
        "phishing_probability": prob,
        "label": "phishing" if prob > 0.5 else "benign",
        "confidence": prob if prob > 0.5 else 1 - prob
    }

@app.get("/health")
def health():
    return {"status": "ok", "models": ["url_xgb", "text_xgb", "meta"]}
