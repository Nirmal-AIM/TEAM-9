"""
Complete ML Pipeline - Training Script
Run this to train the model and generate all artifacts
"""
import pandas as pd
import numpy as np
from pathlib import Path
import config
from data_loader import DataLoader
from model_trainer import CreditScoreModel
from shap_explainer import SHAPExplainer
import joblib

def main():
    print("=" * 60)
    print("🚀 Credit Score ML Pipeline - Training")
    print("=" * 60)
    
    # Step 1: Load Data
    print("\n" + "=" * 60)
    print("STEP 1: Loading Data")
    print("=" * 60)
    loader = DataLoader()
    df = loader.load_data()
    
    # Step 2: Infer Feature Types
    print("\n" + "=" * 60)
    print("STEP 2: Inferring Feature Types")
    print("=" * 60)
    feature_types = loader.infer_feature_types()
    
    # Step 3: Get Features for Modeling
    print("\n" + "=" * 60)
    print("STEP 3: Selecting Features for Modeling")
    print("=" * 60)
    feature_cols = loader.get_features_for_modeling()
    print(f"✅ Selected {len(feature_cols)} features for modeling")
    
    # Step 4: Train Model
    print("\n" + "=" * 60)
    print("STEP 4: Training Credit Score Model")
    print("=" * 60)
    model = CreditScoreModel()
    metrics = model.train(df, feature_cols)
    
    # Step 5: Create SHAP Explainer
    print("\n" + "=" * 60)
    print("STEP 5: Creating SHAP Explainer")
    print("=" * 60)
    
    # Use sample of training data as background
    from sklearn.model_selection import train_test_split
    X_processed = model.preprocessor.transform(df)
    X = X_processed[feature_cols]
    y = model.create_synthetic_target(df)
    X_train, _, _, _ = train_test_split(X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE)
    
    # Use subset for faster SHAP computation
    X_background = X_train.sample(min(100, len(X_train)), random_state=config.RANDOM_STATE)
    
    explainer = SHAPExplainer(model.model, model.preprocessor, feature_cols)
    explainer.create_explainer(X_background.values, explainer_type='tree')
    
    # Step 6: Save Models and Artifacts
    print("\n" + "=" * 60)
    print("STEP 6: Saving Models and Artifacts")
    print("=" * 60)
    
    model_path = config.MODELS_DIR / "credit_score_model.pkl"
    preprocessor_path = config.MODELS_DIR / "preprocessor.pkl"
    explainer_path = config.MODELS_DIR / "shap_explainer.pkl"
    feature_info_path = config.MODELS_DIR / "feature_info.pkl"
    
    model.save(model_path, preprocessor_path)
    
    # Save explainer
    joblib.dump(explainer.explainer, explainer_path)
    print(f"✅ SHAP Explainer saved to {explainer_path}")
    
    # Save feature information
    joblib.dump({
        'feature_names': feature_cols,
        'feature_types': feature_types,
        'metrics': metrics
    }, feature_info_path)
    print(f"✅ Feature info saved to {feature_info_path}")
    
    print("\n" + "=" * 60)
    print("✅ Pipeline Training Complete!")
    print("=" * 60)
    print(f"\n📁 Models saved in: {config.MODELS_DIR}")
    print(f"📊 Model Performance:")
    print(f"   - Test R²: {metrics['test_r2']:.4f}")
    print(f"   - Test RMSE: {metrics['test_rmse']:.2f}")
    print(f"   - Test MAE: {metrics['test_mae']:.2f}")

if __name__ == "__main__":
    main()

