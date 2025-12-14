"""
FastAPI Server for Credit Score ML Model
Provides REST API endpoints for predictions and explanations
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
import uvicorn
from predict import CreditScorePredictor
import config

app = FastAPI(
    title="Credit Score ML API",
    description="API for credit score prediction with SHAP explainability",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor (lazy loading)
predictor = None

def get_predictor():
    """Lazy load predictor"""
    global predictor
    if predictor is None:
        predictor = CreditScorePredictor()
        predictor.load_models()
    return predictor

# Request/Response Models
class UserData(BaseModel):
    """User financial data for prediction"""
    INCOME: Optional[float] = None
    SAVINGS: Optional[float] = None
    DEBT: Optional[float] = None
    R_SAVINGS_INCOME: Optional[float] = None
    R_DEBT_INCOME: Optional[float] = None
    R_DEBT_SAVINGS: Optional[float] = None
    T_CLOTHING_12: Optional[float] = None
    T_EDUCATION_12: Optional[float] = None
    T_ENTERTAINMENT_12: Optional[float] = None
    T_GROCERIES_12: Optional[float] = None
    T_HEALTH_12: Optional[float] = None
    T_HOUSING_12: Optional[float] = None
    T_TRAVEL_12: Optional[float] = None
    T_UTILITIES_12: Optional[float] = None
    T_EXPENDITURE_12: Optional[float] = None
    CAT_GAMBLING: Optional[str] = None
    CAT_DEBT: Optional[int] = None
    CAT_CREDIT_CARD: Optional[int] = None
    CAT_MORTGAGE: Optional[int] = None
    CAT_SAVINGS_ACCOUNT: Optional[int] = None
    CAT_DEPENDENTS: Optional[int] = None
    DEFAULT: Optional[int] = None
    
    class Config:
        extra = "allow"  # Allow additional fields

class PredictionResponse(BaseModel):
    """Response model for credit score prediction"""
    credit_score: int
    category: str
    explanation: Dict

class BatchPredictionRequest(BaseModel):
    """Request for batch predictions"""
    users: List[Dict]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Credit Score ML API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Predict credit score for a single user",
            "/predict/batch": "POST - Predict credit scores for multiple users",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        predictor = get_predictor()
        return {
            "status": "healthy",
            "model_loaded": predictor.model.model is not None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.post("/api/credit-score/analyze", response_model=PredictionResponse)
async def analyze_credit_score(user_data: UserData):
    """
    Analyze credit score for a user with SHAP explanations
    
    Returns:
    - credit_score: Predicted score (300-900)
    - category: Risk category (Excellent, Good, Fair, Poor, Very Poor)
    - explanation: Detailed explanation with factors and recommendations
    """
    try:
        predictor = get_predictor()
        
        # Convert Pydantic model to dict
        user_dict = user_data.dict(exclude_none=True)
        
        # Predict with explanation
        result = predictor.predict_with_explanation(user_dict)
        
        return PredictionResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/api/credit-score/predict")
async def predict_credit_score(user_data: UserData):
    """
    Simple prediction without full explanation (faster)
    """
    try:
        predictor = get_predictor()
        user_dict = user_data.dict(exclude_none=True)
        
        result = predictor.predict_with_explanation(user_dict)
        
        return {
            "score": result['credit_score'],
            "category": result['category']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/api/credit-score/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict credit scores for multiple users
    """
    try:
        predictor = get_predictor()
        result = predictor.predict_batch(request.users)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

@app.get("/api/credit-score/current")
async def get_current_score():
    """
    Get current credit score (placeholder - requires user authentication)
    """
    # This would typically require user authentication
    return {
        "message": "User authentication required",
        "score": None
    }

if __name__ == "__main__":
    print("🚀 Starting Credit Score ML API Server...")
    print(f"📡 Server will run on http://localhost:8000")
    print(f"📚 API docs available at http://localhost:8000/docs")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

