# Credit Score ML Pipeline

Complete Machine Learning pipeline for credit score prediction with SHAP explainability.

## Features

✅ **Data Loading & Feature Inference** - Automatically infers feature types from CSV  
✅ **Data Preprocessing** - Handles missing values, encoding, scaling  
✅ **Synthetic Credit Score Generation** - Creates target variable from financial features  
✅ **ML Model Training** - Gradient Boosting Regressor for score prediction  
✅ **Score Normalization** - Normalizes to 300-900 range  
✅ **User Categorization** - Categorizes users (Excellent, Good, Fair, Poor, Very Poor)  
✅ **SHAP Explainability** - Provides feature importance and explanations  
✅ **Human-Readable Explanations** - Converts SHAP values to natural language  
✅ **REST API** - FastAPI server for frontend integration  

## Project Structure

```
ml_backend/
├── config.py                 # Configuration settings
├── data_loader.py            # Data loading and feature inference
├── preprocessor.py           # Data preprocessing pipeline
├── model_trainer.py          # Model training and synthetic score generation
├── shap_explainer.py         # SHAP explainability module
├── explanation_generator.py   # Human-readable explanation generator
├── predict.py                # Prediction module
├── train_pipeline.py         # Complete training pipeline
├── api_server.py             # FastAPI REST API server
├── requirements.txt          # Python dependencies
├── models/                   # Saved models (created after training)
├── data/                     # Data directory
└── output/                   # Output directory
```

## Installation

1. **Create virtual environment** (recommended):
```bash
cd ml_backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Train the Model

Run the complete training pipeline:

```bash
python train_pipeline.py
```

This will:
- Load and analyze the CSV data
- Infer feature types
- Create synthetic credit scores
- Train the ML model
- Create SHAP explainer
- Save all models and artifacts

### 2. Start API Server

```bash
python api_server.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

### 3. Make Predictions

#### Using Python:
```python
from predict import CreditScorePredictor

predictor = CreditScorePredictor()
predictor.load_models()

user_data = {
    'INCOME': 50000,
    'SAVINGS': 10000,
    'DEBT': 20000,
    # ... other features
}

result = predictor.predict_with_explanation(user_data)
print(f"Credit Score: {result['credit_score']}")
print(f"Category: {result['category']}")
print(f"Explanation: {result['explanation']['explanation_text']}")
```

#### Using API:
```bash
curl -X POST "http://localhost:8000/api/credit-score/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "INCOME": 50000,
    "SAVINGS": 10000,
    "DEBT": 20000
  }'
```

## API Endpoints

### POST `/api/credit-score/analyze`
Predict credit score with full SHAP explanation.

**Request:**
```json
{
  "INCOME": 50000,
  "SAVINGS": 10000,
  "DEBT": 20000,
  "R_DEBT_INCOME": 0.4,
  ...
}
```

**Response:**
```json
{
  "credit_score": 750,
  "category": "Excellent",
  "explanation": {
    "predicted_score": 750,
    "category": "Excellent",
    "positive_factors": [...],
    "negative_factors": [...],
    "recommendations": [...],
    "explanation_text": "..."
  }
}
```

### POST `/api/credit-score/predict`
Simple prediction (faster, no explanation).

### POST `/api/credit-score/predict/batch`
Batch predictions for multiple users.

### GET `/health`
Health check endpoint.

## Model Details

### Synthetic Credit Score Formula

The synthetic credit score is created using:
- **Base Score**: 600
- **Income Factor**: +0 to +100 points
- **Savings Factor**: +0 to +80 points
- **Debt Factor**: -0 to -100 points
- **Debt-to-Income Ratio**: -0 to -50 points
- **Savings-to-Income Ratio**: +0 to +50 points
- **Default Penalty**: -150 points if defaulted
- **Expenditure Ratio**: -0 to -30 points

Final score is normalized to **300-900 range**.

### User Categories

- **Excellent**: 750-900
- **Good**: 700-749
- **Fair**: 650-699
- **Poor**: 600-649
- **Very Poor**: 300-599

## Integration with Frontend

The frontend is already configured to connect to this API. Update `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Then uncomment API calls in:
- `src/hooks/useCreditScore.js`
- `src/components/CreditScoreCard.jsx`

## Model Performance

After training, you'll see metrics like:
- **R² Score**: Model fit quality
- **RMSE**: Root Mean Squared Error
- **MAE**: Mean Absolute Error

## SHAP Explanations

The model provides:
1. **Feature Importance**: Which features matter most
2. **Positive Factors**: What's helping the score
3. **Negative Factors**: What's hurting the score
4. **Recommendations**: Actionable advice to improve
5. **Human-Readable Text**: Natural language explanation

## Next Steps

1. ✅ Train model: `python train_pipeline.py`
2. ✅ Start API: `python api_server.py`
3. ✅ Test predictions
4. ✅ Connect frontend
5. ✅ Deploy to production

## Troubleshooting

- **Model not found**: Run `train_pipeline.py` first
- **Import errors**: Install dependencies with `pip install -r requirements.txt`
- **Port already in use**: Change port in `api_server.py`

