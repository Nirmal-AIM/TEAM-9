"""
Data Preprocessing Module
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import config

class DataPreprocessor:
    """Preprocess data for ML pipeline"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputer = SimpleImputer(strategy='median')
        self.feature_names = []
        self.is_fitted = False
        
    def fit_transform(self, df, feature_cols):
        """Fit preprocessor and transform data"""
        self.feature_names = feature_cols
        
        # Separate numeric and categorical features
        numeric_cols = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df[feature_cols].select_dtypes(include=['object']).columns.tolist()
        
        # Process numeric features
        df_processed = df.copy()
        
        # Handle missing values in numeric columns
        if len(numeric_cols) > 0:
            df_processed[numeric_cols] = self.imputer.fit_transform(df[numeric_cols])
            df_processed[numeric_cols] = pd.DataFrame(
                df_processed[numeric_cols], 
                columns=numeric_cols,
                index=df.index
            )
        
        # Encode categorical features
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df_processed[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        # Scale numeric features
        if len(numeric_cols) > 0:
            df_processed[numeric_cols] = self.scaler.fit_transform(df_processed[numeric_cols])
        
        self.is_fitted = True
        
        return df_processed
    
    def transform(self, df):
        """Transform new data using fitted preprocessor"""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        df_processed = df.copy()
        
        # Get feature columns
        numeric_cols = [col for col in self.feature_names if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
        categorical_cols = [col for col in self.feature_names if col in df.columns and df[col].dtype == 'object']
        
        # Handle missing values
        if len(numeric_cols) > 0:
            df_processed[numeric_cols] = self.imputer.transform(df[numeric_cols])
            df_processed[numeric_cols] = pd.DataFrame(
                df_processed[numeric_cols],
                columns=numeric_cols,
                index=df.index
            )
        
        # Encode categorical
        for col in categorical_cols:
            if col in self.label_encoders:
                le = self.label_encoders[col]
                # Handle unseen categories
                df_processed[col] = df_processed[col].astype(str).apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else 0
                )
        
        # Scale numeric
        if len(numeric_cols) > 0:
            df_processed[numeric_cols] = self.scaler.transform(df_processed[numeric_cols])
        
        return df_processed
    
    def save(self, filepath):
        """Save preprocessor to disk"""
        joblib.dump({
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'imputer': self.imputer,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted
        }, filepath)
        print(f"✅ Preprocessor saved to {filepath}")
    
    def load(self, filepath):
        """Load preprocessor from disk"""
        data = joblib.load(filepath)
        self.scaler = data['scaler']
        self.label_encoders = data['label_encoders']
        self.imputer = data['imputer']
        self.feature_names = data['feature_names']
        self.is_fitted = data['is_fitted']
        print(f"✅ Preprocessor loaded from {filepath}")

