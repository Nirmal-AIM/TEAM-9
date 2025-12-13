"""
Human-Readable Explanation Generator from SHAP Values
"""
import numpy as np
import pandas as pd
from shap_explainer import SHAPExplainer
import config

class ExplanationGenerator:
    """Convert SHAP values into human-readable explanations"""
    
    def __init__(self, explainer, feature_names):
        self.explainer = explainer
        self.feature_names = feature_names
        
        # Feature descriptions for better explanations
        self.feature_descriptions = {
            'INCOME': 'Income Level',
            'SAVINGS': 'Savings Amount',
            'DEBT': 'Total Debt',
            'R_DEBT_INCOME': 'Debt-to-Income Ratio',
            'R_SAVINGS_INCOME': 'Savings-to-Income Ratio',
            'R_DEBT_SAVINGS': 'Debt-to-Savings Ratio',
            'T_EXPENDITURE_12': 'Total Expenditure (12 months)',
            'T_EXPENDITURE_6': 'Total Expenditure (6 months)',
            'DEFAULT': 'Default History',
            'CAT_CREDIT_CARD': 'Credit Card Usage',
            'CAT_MORTGAGE': 'Mortgage Status',
            'CAT_SAVINGS_ACCOUNT': 'Savings Account',
            'CAT_DEPENDENTS': 'Number of Dependents'
        }
    
    def generate_explanation(self, shap_values, feature_values, predicted_score, base_score=None):
        """
        Generate human-readable explanation from SHAP values
        
        Args:
            shap_values: SHAP values for the prediction (array)
            feature_values: Actual feature values (dict or Series)
            predicted_score: Predicted credit score
            base_score: Base/expected score (optional)
        
        Returns:
            Dictionary with explanation components
        """
        if isinstance(shap_values, np.ndarray):
            shap_values = shap_values.flatten()
        
        if isinstance(feature_values, pd.Series):
            feature_values = feature_values.to_dict()
        
        # Get feature importance (absolute SHAP values)
        feature_importance = np.abs(shap_values)
        
        # Get top contributing features
        top_indices = np.argsort(feature_importance)[::-1][:10]  # Top 10 features
        
        # Categorize factors
        positive_factors = []
        negative_factors = []
        
        for idx in top_indices:
            feature_name = self.feature_names[idx]
            shap_value = shap_values[idx]
            feature_value = feature_values.get(feature_name, 'N/A')
            
            description = self.feature_descriptions.get(feature_name, feature_name)
            
            factor_info = {
                'feature': feature_name,
                'description': description,
                'impact': float(shap_value),
                'value': feature_value
            }
            
            if shap_value > 0:
                positive_factors.append(factor_info)
            else:
                negative_factors.append(factor_info)
        
        # Generate summary
        total_positive_impact = sum([f['impact'] for f in positive_factors])
        total_negative_impact = sum([f['impact'] for f in negative_factors])
        
        # Generate recommendations
        recommendations = self._generate_recommendations(negative_factors, feature_values)
        
        # Generate explanation text
        explanation_text = self._generate_explanation_text(
            predicted_score,
            positive_factors[:5],
            negative_factors[:5],
            total_positive_impact,
            total_negative_impact,
            recommendations
        )
        
        return {
            'predicted_score': int(predicted_score),
            'category': self._categorize_score(predicted_score),
            'base_score': float(base_score) if base_score else None,
            'positive_factors': positive_factors[:5],
            'negative_factors': negative_factors[:5],
            'total_positive_impact': float(total_positive_impact),
            'total_negative_impact': float(total_negative_impact),
            'recommendations': recommendations,
            'explanation_text': explanation_text,
            'all_features': [
                {
                    'feature': self.feature_names[i],
                    'description': self.feature_descriptions.get(self.feature_names[i], self.feature_names[i]),
                    'shap_value': float(shap_values[i]),
                    'value': feature_values.get(self.feature_names[i], 'N/A')
                }
                for i in range(len(self.feature_names))
            ]
        }
    
    def _categorize_score(self, score):
        """Categorize credit score"""
        for category, (min_score, max_score) in config.CREDIT_CATEGORIES.items():
            if min_score <= score <= max_score:
                return category
        return "Unknown"
    
    def _generate_recommendations(self, negative_factors, feature_values):
        """Generate actionable recommendations based on negative factors"""
        recommendations = []
        
        for factor in negative_factors[:5]:  # Top 5 negative factors
            feature = factor['feature']
            
            if 'DEBT' in feature and 'INCOME' not in feature:
                recommendations.append({
                    'priority': 'High',
                    'action': 'Reduce total debt',
                    'reason': f"High debt ({factor['value']}) is negatively impacting your score",
                    'impact': 'High'
                })
            elif 'R_DEBT_INCOME' in feature:
                recommendations.append({
                    'priority': 'High',
                    'action': 'Lower debt-to-income ratio',
                    'reason': f"Your debt-to-income ratio ({factor['value']:.2f}) is too high",
                    'impact': 'High'
                })
            elif 'SAVINGS' in feature and 'INCOME' not in feature:
                recommendations.append({
                    'priority': 'Medium',
                    'action': 'Increase savings',
                    'reason': f"Low savings ({factor['value']}) affects your creditworthiness",
                    'impact': 'Medium'
                })
            elif 'DEFAULT' in feature:
                recommendations.append({
                    'priority': 'Critical',
                    'action': 'Address default history',
                    'reason': 'Previous defaults significantly impact your credit score',
                    'impact': 'Critical'
                })
            elif 'EXPENDITURE' in feature:
                recommendations.append({
                    'priority': 'Medium',
                    'action': 'Reduce unnecessary spending',
                    'reason': f"High expenditure relative to income affects your score",
                    'impact': 'Medium'
                })
        
        # Add general recommendations if none specific
        if not recommendations:
            recommendations.append({
                'priority': 'Medium',
                'action': 'Maintain consistent payment history',
                'reason': 'Regular payments improve credit score over time',
                'impact': 'Medium'
            })
        
        return recommendations[:5]  # Return top 5
    
    def _generate_explanation_text(self, score, positive_factors, negative_factors, 
                                   pos_impact, neg_impact, recommendations):
        """Generate natural language explanation"""
        category = self._categorize_score(score)
        
        text = f"Your credit score is {int(score)}, which falls in the '{category}' category.\n\n"
        
        if positive_factors:
            text += "Factors positively impacting your score:\n"
            for i, factor in enumerate(positive_factors[:3], 1):
                text += f"{i}. {factor['description']} contributes +{factor['impact']:.1f} points\n"
            text += "\n"
        
        if negative_factors:
            text += "Factors negatively impacting your score:\n"
            for i, factor in enumerate(negative_factors[:3], 1):
                text += f"{i}. {factor['description']} reduces your score by {abs(factor['impact']):.1f} points\n"
            text += "\n"
        
        if recommendations:
            text += "Recommendations to improve your score:\n"
            for i, rec in enumerate(recommendations[:3], 1):
                text += f"{i}. {rec['action']} - {rec['reason']}\n"
        
        return text

