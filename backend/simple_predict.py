import pandas as pd
import pickle
import os
import sys

def predict_now(user_id='C03PVPPHOY'):
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, 'credit_score_model.pkl')
    csv_path = os.path.join(base_dir, '../public/credit_score.csv')

    print(f"--- Loading Resources ---")
    if not os.path.exists(model_path):
        print("Model not found. Please run train_model.py first.")
        return

    with open(model_path, 'rb') as f:
        artifacts = pickle.load(f)
    print("Model loaded.")

    df = pd.read_csv(csv_path)
    print(f"Dataset loaded. Found {len(df)} records.")
    
    # Find user
    user = df[df['CUST_ID'] == user_id]
    if user.empty:
        print(f"User {user_id} not found.")
        return
        
    print(f"\n--- Analyzing User: {user_id} ---")
    user_data = user.iloc[0].to_dict()
    
    # Prepare input
    model = artifacts['model']
    features = artifacts['features']
    label_encoders = artifacts['label_encoders']
    
    input_vector = []
    for feat in features:
        val = user_data.get(feat, 0)
        if feat in label_encoders:
            le = label_encoders[feat]
            try:
                val = le.transform([str(val)])[0]
            except:
                val = 0
        input_vector.append(float(val))
    
    # Predict
    score = model.predict([input_vector])[0]
    
    print(f"\nPREDICTED CREDIT SCORE: {int(score)}")
    print("-" * 30)
    
    # Simple logic explanation
    print("Key Factors:")
    importances = list(zip(features, model.feature_importances_))
    importances.sort(key=lambda x: x[1], reverse=True)
    
    for feat, imp in importances[:3]:
        print(f"- {feat}: {user_data.get(feat, 'N/A')}")
        
    print("-" * 30)
    print("Recommendation:")
    if score < 600:
        print("Focus on paying off debts and avoid new loans.")
    elif score < 750:
        print("Good standing. Keep utilization low to improve further.")
    else:
        print("Excellent score! Maintain your current habits.")

if __name__ == "__main__":
    target_user = sys.argv[1] if len(sys.argv) > 1 else 'C03PVPPHOY'
    predict_now(target_user)
