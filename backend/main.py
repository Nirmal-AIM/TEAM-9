from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import os
import numpy as np

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model and Data
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'credit_score_model.pkl')
CSV_PATH = os.path.join(BASE_DIR, '../public/credit_score.csv')

model_artifacts = None
df_data = None

def load_resources():
    global model_artifacts, df_data
    try:
        with open(MODEL_PATH, 'rb') as f:
            model_artifacts = pickle.load(f)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

    try:
        df_data = pd.read_csv(CSV_PATH)
        # Create an index for faster lookup
        if 'CUST_ID' in df_data.columns:
            df_data.set_index('CUST_ID', inplace=True)
        print("CSV data loaded successfully.")
    except Exception as e:
        print(f"Error loading CSV data: {e}")

load_resources()

class AnalyzeRequest(BaseModel):
    # Dynamic fields - we will convert incoming JSON to DataFrame
    features: dict

@app.get("/")
def read_root():
    return {"message": "Credit Score ML API is running"}

@app.get("/api/user/{user_id}")
def get_user_data(user_id: str):
    if df_data is None or user_id not in df_data.index:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_row = df_data.loc[user_id]
    user_dict = user_row.to_dict()
    
    # We can also run the explanation logic here
    explanation = generate_explanation(user_dict)
    
    return {
        "user_id": user_id,
        "data": user_dict,
        "explanation": explanation
    }

@app.post("/api/credit-score/analyze")
def analyze_score(request: AnalyzeRequest):
    # This endpoint allows analyzing custom input data
    explanation = generate_explanation(request.features)
    return explanation

def generate_explanation(user_data):
    if model_artifacts is None:
        return {"error": "Model not loaded"}
    
    model = model_artifacts['model']
    feature_names = model_artifacts['features']
    label_encoders = model_artifacts['label_encoders']
    
    # Prepare input vector
    input_data = []
    
    # We need to fill missing features with defaults or 0 if not provided
    # and encode categoricals
    
    processed_row = {}
    
    for feat in feature_names:
        val = user_data.get(feat, 0)
        
        # Handle encoding
        if feat in label_encoders:
            le = label_encoders[feat]
            try:
                val = str(val)
                # Handle unknown labels if necessary, for now try/except
                if val in le.classes_:
                    val = le.transform([val])[0]
                else:
                    val = 0 # Fallback
            except:
                val = 0
                
        processed_row[feat] = float(val) if isinstance(val, (int, float)) else val
        input_data.append(processed_row[feat])
        
    # Predict
    prediction = model.predict([input_data])[0]
    
    # Explanation Logic
    # 1. Feature Importance (Global)
    importances = list(zip(feature_names, model.feature_importances_))
    importances.sort(key=lambda x: x[1], reverse=True)
    top_features = importances[:3]
    
    # 2. Local Explanation (Simple)
    # Compare user values to average? 
    # Or just explain based on high leverage features.
    
    why_text = []
    improve_text = []
    
    # Simple heuristic: meaningful factors
    for feat, imp in top_features:
        val = processed_row[feat]
        # Just a generic explanation for now based on feature name
        # Ideally we'd know directionality (SHAP values), but for this quick impl:
        why_text.append(f"{feat} (Importance: {imp:.2f}) plays a major role.")
        
        # Heuristics for common fields
        feat_upper = feat.upper()
        if 'DEBT' in feat_upper:
             improve_text.append(f"Lowering your {feat} usually improves the score.")
        elif 'SAVINGS' in feat_upper or 'INCOME' in feat_upper:
             improve_text.append(f"Increasing {feat} can help.")
        elif 'GAMBLING' in feat_upper:
             improve_text.append(f"Reducing {feat} is recommended.")
             
    if not improve_text:
        improve_text.append("Maintain good financial habits.")
        
    return {
        "score": round(prediction, 1),
        "analysis": {
            "factors": [f"{f}: {v}" for f, v in zip(feature_names, input_data) if f in [tf[0] for tf in top_features]],
            "explanation": " ".join(why_text),
            "recommendations": improve_text
        }
    }
