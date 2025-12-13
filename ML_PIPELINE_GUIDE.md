# Complete ML Pipeline Guide

## Overview

This ML pipeline creates a **synthetic credit score prediction system** with full explainability using SHAP values.

## What It Does

1. ✅ **Reads `credit_score.csv`** - Loads your dataset
2. ✅ **Infers Feature Types** - Automatically detects numeric, categorical, binary, ratio features
3. ✅ **Creates Synthetic Credit Score** - Generates target variable (300-900 range)
4. ✅ **Preprocesses Data** - Handles missing values, encoding, scaling
5. ✅ **Trains ML Model** - Gradient Boosting Regressor
6. ✅ **Normalizes Scores** - Ensures 300-900 range
7. ✅ **Categorizes Users** - Excellent, Good, Fair, Poor, Very Poor
8. ✅ **SHAP Explainability** - Feature importance and impact
9. ✅ **Human-Readable Explanations** - Natural language insights

## Quick Start

### Step 1: Install Dependencies

```bash
cd ml_backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Train the Model

```bash
python train_pipeline.py
```

This will:
- Load and analyze your CSV
- Create synthetic credit scores
- Train the ML model
- Generate SHAP explainer
- Save all models

### Step 3: Start API Server

```bash
python api_server.py
```

API available at: **http://localhost:8000**

## Pipeline Components

### 1. Data Loader (`data_loader.py`)
- Loads CSV file
- Infers feature types automatically
- Identifies ID, numeric, categorical, binary, ratio columns

### 2. Preprocessor (`preprocessor.py`)
- Handles missing values (median imputation)
- Encodes categorical variables
- Scales numeric features
- Saves/loads preprocessing pipeline

### 3. Model Trainer (`model_trainer.py`)
- **Creates Synthetic Credit Score**:
  - Base: 600 points
  - Income: +0 to +100
  - Savings: +0 to +80
  - Debt: -0 to -100
  - Debt-to-Income: -0 to -50
  - Savings-to-Income: +0 to +50
  - Default: -150 if defaulted
  - Expenditure: -0 to -30
  - **Normalized to 300-900 range**

- Trains Gradient Boosting Regressor
- Categorizes scores into risk levels

### 4. SHAP Explainer (`shap_explainer.py`)
- Creates TreeExplainer for fast SHAP computation
- Generates feature importance values
- Explains individual predictions

### 5. Explanation Generator (`explanation_generator.py`)
- Converts SHAP values to human language
- Identifies positive/negative factors
- Generates actionable recommendations
- Creates natural language explanations

### 6. API Server (`api_server.py`)
- FastAPI REST API
- Endpoints for predictions
- CORS enabled for frontend
- Auto-generated API docs

## API Integration

### Frontend Connection

Your React frontend is already configured! Just:

1. **Train the model** (if not done):
```bash
cd ml_backend
python train_pipeline.py
```

2. **Start API server**:
```bash
python api_server.py
```

3. **Update frontend** `.env`:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

4. **Uncomment API calls** in:
   - `src/hooks/useCreditScore.js`
   - `src/components/CreditScoreCard.jsx`

## Example API Usage

### Predict Credit Score

```bash
curl -X POST "http://localhost:8000/api/credit-score/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "INCOME": 50000,
    "SAVINGS": 10000,
    "DEBT": 20000,
    "R_DEBT_INCOME": 0.4,
    "R_SAVINGS_INCOME": 0.2,
    "DEFAULT": 0
  }'
```

### Response Example

```json
{
  "credit_score": 750,
  "category": "Excellent",
  "explanation": {
    "predicted_score": 750,
    "category": "Excellent",
    "positive_factors": [
      {
        "feature": "SAVINGS",
        "description": "Savings Amount",
        "impact": 15.5,
        "value": 10000
      }
    ],
    "negative_factors": [
      {
        "feature": "DEBT",
        "description": "Total Debt",
        "impact": -8.2,
        "value": 20000
      }
    ],
    "recommendations": [
      {
        "priority": "Medium",
        "action": "Reduce total debt",
        "reason": "High debt (20000) is negatively impacting your score",
        "impact": "High"
      }
    ],
    "explanation_text": "Your credit score is 750, which falls in the 'Excellent' category..."
  }
}
```

## Model Output Structure

### Credit Score
- **Range**: 300-900
- **Normalized**: Yes
- **Based on**: Financial features and ratios

### Categories
- **Excellent**: 750-900
- **Good**: 700-749
- **Fair**: 650-699
- **Poor**: 600-649
- **Very Poor**: 300-599

### Explanations Include
1. **Predicted Score** - The credit score
2. **Category** - Risk category
3. **Positive Factors** - What's helping (top 5)
4. **Negative Factors** - What's hurting (top 5)
5. **Recommendations** - Actionable advice
6. **Explanation Text** - Natural language summary

## File Structure

```
ml_backend/
├── config.py                    # Configuration
├── data_loader.py              # Data loading & feature inference
├── preprocessor.py             # Data preprocessing
├── model_trainer.py            # Model training & synthetic score
├── shap_explainer.py           # SHAP explainability
├── explanation_generator.py    # Human-readable explanations
├── predict.py                  # Prediction module
├── train_pipeline.py           # Complete training script
├── api_server.py               # FastAPI server
├── requirements.txt            # Dependencies
├── README.md                   # Detailed documentation
└── models/                     # Saved models (after training)
    ├── credit_score_model.pkl
    ├── preprocessor.pkl
    ├── shap_explainer.pkl
    └── feature_info.pkl
```

## Next Steps

1. ✅ **Train Model**: `python train_pipeline.py`
2. ✅ **Start API**: `python api_server.py`
3. ✅ **Test API**: Visit http://localhost:8000/docs
4. ✅ **Connect Frontend**: Update `.env` and uncomment API calls
5. ✅ **Test Integration**: Use "Analyze Score" button in frontend

## Troubleshooting

- **Module not found**: Install dependencies with `pip install -r requirements.txt`
- **Model not found**: Run `train_pipeline.py` first
- **Port in use**: Change port in `api_server.py`
- **CSV not found**: Ensure `public/credit_score.csv` exists

## Model Performance

After training, check:
- **R² Score**: Should be > 0.7 (good fit)
- **RMSE**: Lower is better
- **MAE**: Mean absolute error

The model learns patterns from your synthetic credit scores and can predict scores for new users with explanations!

