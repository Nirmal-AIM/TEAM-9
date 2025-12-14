"""
Data Loading and Feature Type Inference Module
"""
import pandas as pd
import numpy as np
from pathlib import Path
import config

class DataLoader:
    """Load and infer feature types from credit score dataset"""
    
    def __init__(self, csv_path=None):
        self.csv_path = csv_path or config.CSV_FILE_PATH
        self.df = None
        self.feature_types = {}
        
    def load_data(self):
        """Load CSV data"""
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"✅ Loaded {len(self.df)} records with {len(self.df.columns)} columns")
            return self.df
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def infer_feature_types(self):
        """Automatically infer feature types from data"""
        if self.df is None:
            self.load_data()
        
        feature_types = {
            'numeric': [],
            'categorical': [],
            'binary': [],
            'ratio': [],
            'id': []
        }
        
        for col in self.df.columns:
            # ID columns
            if 'ID' in col.upper() or col.upper() == 'CUST_ID':
                feature_types['id'].append(col)
            
            # Binary columns (0/1, Yes/No, High/Low)
            elif self.df[col].dtype == 'object':
                unique_vals = self.df[col].nunique()
                if unique_vals <= 3:
                    feature_types['binary'].append(col)
                else:
                    feature_types['categorical'].append(col)
            
            # Ratio columns (R_ prefix)
            elif col.startswith('R_'):
                feature_types['ratio'].append(col)
            
            # Numeric columns
            elif pd.api.types.is_numeric_dtype(self.df[col]):
                feature_types['numeric'].append(col)
        
        self.feature_types = feature_types
        
        print("\n📊 Feature Type Inference:")
        print(f"  - ID columns: {len(feature_types['id'])}")
        print(f"  - Numeric columns: {len(feature_types['numeric'])}")
        print(f"  - Categorical columns: {len(feature_types['categorical'])}")
        print(f"  - Binary columns: {len(feature_types['binary'])}")
        print(f"  - Ratio columns: {len(feature_types['ratio'])}")
        
        return feature_types
    
    def get_features_for_modeling(self):
        """Get features suitable for ML modeling (exclude ID and target columns)"""
        exclude_cols = ['CUST_ID', 'CREDIT_SCORE', 'DEFAULT']
        
        # Get all columns except excluded ones
        feature_cols = [col for col in self.df.columns if col not in exclude_cols]
        
        return feature_cols
    
    def get_data_summary(self):
        """Get summary statistics of the dataset"""
        if self.df is None:
            self.load_data()
        
        summary = {
            'total_records': len(self.df),
            'total_features': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'numeric_stats': self.df.select_dtypes(include=[np.number]).describe().to_dict()
        }
        
        return summary

