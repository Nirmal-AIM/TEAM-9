"""
ML Model Training Module - Creates Synthetic Credit Score
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import config
from preprocessor import DataPreprocessor
from data_loader import DataLoader

class CreditScoreModel:
    """Train and manage credit score prediction model"""
    
    def __init__(self):
        self.model = None
        self.preprocessor = DataPreprocessor()
        self.feature_names = []
        
    def create_synthetic_target(self, df):
        """
        Create synthetic credit score based on financial features
        Uses weighted combination of key financial indicators
        """
        # Key factors for credit score calculation
        score = 600  # Base score
        
        # Income factor (0-100 points)
        if 'INCOME' in df.columns:
            income_normalized = (df['INCOME'] - df['INCOME'].min()) / (df['INCOME'].max() - df['INCOME'].min() + 1e-10)
            score += income_normalized * 100
        
        # Savings factor (0-80 points)
        if 'SAVINGS' in df.columns:
            savings_normalized = (df['SAVINGS'] - df['SAVINGS'].min()) / (df['SAVINGS'].max() - df['SAVINGS'].min() + 1e-10)
            score += savings_normalized * 80
        
        # Debt factor (negative impact, -100 to 0 points)
        if 'DEBT' in df.columns:
            debt_normalized = (df['DEBT'] - df['DEBT'].min()) / (df['DEBT'].max() - df['DEBT'].min() + 1e-10)
            score -= debt_normalized * 100
        
        # Debt-to-Income ratio (negative impact, -50 to 0 points)
        if 'R_DEBT_INCOME' in df.columns:
            debt_income_ratio = df['R_DEBT_INCOME'].clip(0, 20) / 20  # Normalize to 0-1
            score -= debt_income_ratio * 50
        
        # Savings-to-Income ratio (positive impact, 0-50 points)
        if 'R_SAVINGS_INCOME' in df.columns:
            savings_income_ratio = df['R_SAVINGS_INCOME'].clip(0, 10) / 10  # Normalize to 0-1
            score += savings_income_ratio * 50
        
        # Default status (major negative impact, -150 points)
        if 'DEFAULT' in df.columns:
            default_penalty = df['DEFAULT'].apply(lambda x: -150 if str(x) == '1' else 0)
            score += default_penalty
        
        # Spending patterns (moderate impact)
        if 'T_EXPENDITURE_12' in df.columns and 'INCOME' in df.columns:
            expenditure_ratio = (df['T_EXPENDITURE_12'] / (df['INCOME'] + 1)).clip(0, 2) / 2
            score -= expenditure_ratio * 30  # High spending relative to income is negative
        
        # Normalize to 300-900 range
        score = score.clip(300, 900)
        
        return score.astype(int)
    
    def train(self, df, feature_cols):
        """Train the credit score prediction model"""
        print("\n🚀 Training Credit Score Model...")
        
        # Create synthetic target
        print("📊 Creating synthetic credit score...")
        y = self.create_synthetic_target(df)
        
        print(f"   Score range: {y.min()} - {y.max()}")
        print(f"   Mean score: {y.mean():.2f}")
        print(f"   Std score: {y.std():.2f}")
        
        # Preprocess features
        print("\n🔧 Preprocessing features...")
        X_processed = self.preprocessor.fit_transform(df, feature_cols)
        X = X_processed[feature_cols]
        
        self.feature_names = feature_cols
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
        )
        
        print(f"\n📈 Training set: {len(X_train)} samples")
        print(f"📊 Test set: {len(X_test)} samples")
        
        # Train model (using Gradient Boosting for better performance)
        print("\n🎯 Training Gradient Boosting Regressor...")
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=config.RANDOM_STATE,
            subsample=0.8
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        
        print("\n📊 Model Performance:")
        print(f"   Train RMSE: {train_rmse:.2f}")
        print(f"   Test RMSE: {test_rmse:.2f}")
        print(f"   Train R²: {train_r2:.4f}")
        print(f"   Test R²: {test_r2:.4f}")
        print(f"   Test MAE: {test_mae:.2f}")
        
        return {
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'test_mae': test_mae
        }
    
    def predict(self, df):
        """Predict credit scores for new data"""
        if self.model is None:
            raise ValueError("Model must be trained before prediction")
        
        X_processed = self.preprocessor.transform(df)
        X = X_processed[self.feature_names]
        
        predictions = self.model.predict(X)
        # Ensure predictions are in valid range
        predictions = np.clip(predictions, config.CREDIT_SCORE_MIN, config.CREDIT_SCORE_MAX)
        
        return predictions.astype(int)
    
    def categorize_score(self, score):
        """Categorize credit score into risk categories"""
        for category, (min_score, max_score) in config.CREDIT_CATEGORIES.items():
            if min_score <= score <= max_score:
                return category
        return "Unknown"
    
    def save(self, model_path, preprocessor_path):
        """Save model and preprocessor"""
        joblib.dump(self.model, model_path)
        self.preprocessor.save(preprocessor_path)
        print(f"\n✅ Model saved to {model_path}")
        print(f"✅ Preprocessor saved to {preprocessor_path}")
    
    def load(self, model_path, preprocessor_path):
        """Load model and preprocessor"""
        self.model = joblib.load(model_path)
        self.preprocessor.load(preprocessor_path)
        self.feature_names = self.preprocessor.feature_names
        print(f"\n✅ Model loaded from {model_path}")
        print(f"✅ Preprocessor loaded from {preprocessor_path}")

