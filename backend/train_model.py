import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_model():
    # Load dataset
    csv_path = os.path.join(os.path.dirname(__file__), '../public/credit_score.csv')
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Identify relevant columns
    # We want to predict CREDIT_SCORE based on other factors
    # Assuming columns like INCOME, SAVINGS, DEBT, RENT, BILLS, etc. exist.
    # We will dynamically select numeric columns and handle some categorical ones if they exist.
    
    # Drop IDs and target from features
    target_col = 'CREDIT_SCORE'
    drop_cols = ['CUST_ID', target_col, 'DEFAULT', 'CAT_GAMBLING', 'CAT_DEBT', 'CAT_CREDIT_CARD', 'CAT_MORTGAGE', 'CAT_SAVINGS', 'CAT_DEPENDENTS', 'CAT_INSURANCE', 'CAT_RATING'] # Drop potential non-numeric or target leakage cols if they exist
    
    # Select features
    # First, let's see what we actually have.
    # For now, we'll try to use everything except ID and target, converting categoricals.
    
    feature_df = df.drop(columns=[c for c in ['CUST_ID', target_col] if c in df.columns])
    
    # Simple preprocessing: Label Encode object columns
    label_encoders = {}
    for col in feature_df.columns:
        if feature_df[col].dtype == 'object':
            le = LabelEncoder()
            feature_df[col] = le.fit_transform(feature_df[col].astype(str))
            label_encoders[col] = le
            
    X = feature_df
    y = df[target_col]
    
    # Train model
    print("Training Random Forest model...")
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    # Save artifacts
    artifacts = {
        'model': rf,
        'features': X.columns.tolist(),
        'label_encoders': label_encoders
    }
    
    output_path = os.path.join(os.path.dirname(__file__), 'credit_score_model.pkl')
    with open(output_path, 'wb') as f:
        pickle.dump(artifacts, f)
        
    print(f"Model saved to {output_path}")
    print("Feature Importances:")
    importances = list(zip(X.columns, rf.feature_importances_))
    importances.sort(key=lambda x: x[1], reverse=True)
    for feat, imp in importances[:5]:
        print(f"{feat}: {imp:.4f}")

if __name__ == "__main__":
    train_model()
