"""
SHAP Explainability Module
"""
import numpy as np
import pandas as pd
import shap
import joblib
from model_trainer import CreditScoreModel
import config

class SHAPExplainer:
    """Generate SHAP explanations for credit score predictions"""
    
    def __init__(self, model, preprocessor, feature_names):
        self.model = model
        self.preprocessor = preprocessor
        self.feature_names = feature_names
        self.explainer = None
        self.shap_values = None
        
    def create_explainer(self, X_background, explainer_type='tree'):
        """
        Create SHAP explainer
        X_background: Background dataset for SHAP (sample of training data)
        """
        print("\n🔍 Creating SHAP Explainer...")
        
        if explainer_type == 'tree':
            # TreeExplainer for tree-based models (faster)
            self.explainer = shap.TreeExplainer(self.model)
        else:
            # KernelExplainer (slower but works for any model)
            self.explainer = shap.KernelExplainer(
                self.model.predict,
                X_background
            )
        
        print("✅ SHAP Explainer created")
        return self.explainer
    
    def explain_prediction(self, X_instance):
        """
        Generate SHAP values for a single prediction
        X_instance: Single row of features (DataFrame or array)
        """
        if self.explainer is None:
            raise ValueError("Explainer must be created first. Call create_explainer()")
        
        # Ensure X_instance is in correct format
        if isinstance(X_instance, pd.DataFrame):
            X_instance = X_instance[self.feature_names]
        else:
            X_instance = pd.DataFrame(X_instance, columns=self.feature_names)
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X_instance)
        
        # Handle array format
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        
        return shap_values
    
    def explain_batch(self, X_batch):
        """Generate SHAP values for multiple predictions"""
        if self.explainer is None:
            raise ValueError("Explainer must be created first. Call create_explainer()")
        
        if isinstance(X_batch, pd.DataFrame):
            X_batch = X_batch[self.feature_names]
        
        shap_values = self.explainer.shap_values(X_batch)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        
        return shap_values

