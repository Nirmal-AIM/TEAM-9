"""
Prediction Module - Use trained model to predict credit scores
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import config
from model_trainer import CreditScoreModel
from shap_explainer import SHAPExplainer
from explanation_generator import ExplanationGenerator

class CreditScorePredictor:
    """Predict credit scores with SHAP explanations"""
    
    def __init__(self):
        self.model = CreditScoreModel()
        self.explainer = None
        self.explanation_generator = None
        self.feature_names = []
        
    def load_models(self):
        """Load trained models and explainers"""
        model_path = config.MODELS_DIR / "credit_score_model.pkl"
        preprocessor_path = config.MODELS_DIR / "preprocessor.pkl"
        explainer_path = config.MODELS_DIR / "shap_explainer.pkl"
        feature_info_path = config.MODELS_DIR / "feature_info.pkl"
        
        # Load model
        self.model.load(model_path, preprocessor_path)
        self.feature_names = self.model.feature_names
        
        # Load explainer
        self.explainer = SHAPExplainer(
            self.model.model,
            self.model.preprocessor,
            self.feature_names
        )
        self.explainer.explainer = joblib.load(explainer_path)
        
        # Load feature info
        feature_info = joblib.load(feature_info_path)
        
        # Create explanation generator
        self.explanation_generator = ExplanationGenerator(
            self.explainer.explainer,
            self.feature_names
        )
        
        print("✅ All models loaded successfully")
    
    def predict_with_explanation(self, user_data):
        """
        Predict credit score with full explanation
        
        Args:
            user_data: Dictionary or DataFrame with user features
        
        Returns:
            Dictionary with prediction and explanation
        """
        if self.model.model is None:
            self.load_models()
        
        # Convert to DataFrame if needed
        if isinstance(user_data, dict):
            user_df = pd.DataFrame([user_data])
        else:
            user_df = user_data.copy()
        
        # Predict score
        predictions = self.model.predict(user_df)
        predicted_score = int(predictions[0])
        
        # Get SHAP values
        X_processed = self.model.preprocessor.transform(user_df)
        X = X_processed[self.feature_names]
        shap_values = self.explainer.explain_prediction(X)
        
        # Get base value (expected value)
        base_value = self.explainer.explainer.expected_value
        if isinstance(base_value, np.ndarray):
            base_value = base_value[0]
        
        # Generate explanation
        feature_values = user_df.iloc[0].to_dict()
        explanation = self.explanation_generator.generate_explanation(
            shap_values,
            feature_values,
            predicted_score,
            base_value
        )
        
        return {
            'credit_score': predicted_score,
            'category': explanation['category'],
            'explanation': explanation
        }
    
    def predict_batch(self, user_data_batch):
        """Predict scores for multiple users"""
        if self.model.model is None:
            self.load_models()
        
        if isinstance(user_data_batch, list):
            user_df = pd.DataFrame(user_data_batch)
        else:
            user_df = user_data_batch.copy()
        
        predictions = self.model.predict(user_df)
        categories = [self.model.categorize_score(score) for score in predictions]
        
        return {
            'scores': predictions.tolist(),
            'categories': categories
        }

# Example usage
if __name__ == "__main__":
    # Load a sample user from CSV for testing
    from data_loader import DataLoader
    
    loader = DataLoader()
    df = loader.load_data()
    
    # Test with first user
    test_user = df.iloc[0].to_dict()
    
    predictor = CreditScorePredictor()
    result = predictor.predict_with_explanation(test_user)
    
    print("\n" + "=" * 60)
    print("Prediction Result")
    print("=" * 60)
    print(f"Credit Score: {result['credit_score']}")
    print(f"Category: {result['category']}")
    print(f"\nExplanation:\n{result['explanation']['explanation_text']}")

