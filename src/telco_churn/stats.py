"""
Statistical Analysis Module - What Separates Data Analysts from Data Scientists

LEARNING NOTES:
- Statistical validation prevents false conclusions
- Effect size matters more than p-values in business contexts  
- Different tests for different data types and assumptions

INTERVIEW TALKING POINTS:
- "I validate insights with appropriate statistical tests"
- "I check assumptions before applying parametric tests"
- "I report effect sizes alongside significance"
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, ttest_ind, mannwhitneyu
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

def perform_statistical_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Comprehensive statistical analysis of Telco data.
    
    This demonstrates understanding of:
    - Hypothesis testing
    - Effect sizes
    - Appropriate test selection
    - Business interpretation
    """
    results = {}
    
    # 1. Test numerical features vs churn
    numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    results['numerical_tests'] = {}
    
    for feature in numerical_features:
        if feature in df.columns:
            results['numerical_tests'][feature] = test_numerical_vs_churn(
                df, feature, 'Churn'
            )
    
    # 2. Test categorical features vs churn  
    categorical_features = ['Contract', 'PaymentMethod', 'InternetService']
    results['categorical_tests'] = {}
    
    for feature in categorical_features:
        if feature in df.columns:
            results['categorical_tests'][feature] = test_categorical_vs_churn(
                df, feature, 'Churn'
            )
    
    # 3. Identify high-risk segments
    results['risk_segments'] = identify_risk_segments(df)
    
    return results


def test_numerical_vs_churn(
    df: pd.DataFrame,
    numerical_col: str,
    target_col: str = 'Churn'
) -> Dict[str, Any]:
    """
    Test if numerical feature differs between churn groups.
    
    STATISTICAL DECISION TREE:
    1. Test normality (Shapiro-Wilk)
    2. If normal: use t-test (parametric)
    3. If not normal: use Mann-Whitney U (non-parametric)
    4. Always report effect size (Cohen's d)
    
    This shows you understand test assumptions!
    """
    churned = df[df[target_col] == 'Yes'][numerical_col].dropna()
    retained = df[df[target_col] == 'No'][numerical_col].dropna()
    
    # Test normality
    _, p_normality_churned = stats.shapiro(churned.sample(min(100, len(churned))))
    _, p_normality_retained = stats.shapiro(retained.sample(min(100, len(retained))))
    
    is_normal = (p_normality_churned > 0.05) and (p_normality_retained > 0.05)
    
    # Choose appropriate test
    if is_normal:
        statistic, p_value = ttest_ind(churned, retained)
        test_used = 't-test'
    else:
        statistic, p_value = mannwhitneyu(churned, retained)
        test_used = 'Mann-Whitney U'
    
    # Calculate effect size (Cohen's d)
    pooled_std = np.sqrt(((len(churned)-1)*churned.std()**2 + 
                          (len(retained)-1)*retained.std()**2) / 
                         (len(churned) + len(retained) - 2))
    cohens_d = (churned.mean() - retained.mean()) / pooled_std
    
    # Interpret effect size
    if abs(cohens_d) < 0.2:
        effect_interpretation = "negligible"
    elif abs(cohens_d) < 0.5:
        effect_interpretation = "small"
    elif abs(cohens_d) < 0.8:
        effect_interpretation = "medium"
    else:
        effect_interpretation = "large"
    
    return {
        'test_used': test_used,
        'statistic': float(statistic),
        'p_value': float(p_value),
        'significant': p_value < 0.05,
        'churned_mean': float(churned.mean()),
        'retained_mean': float(retained.mean()),
        'cohens_d': float(cohens_d),
        'effect_size': effect_interpretation,
        'sample_sizes': {'churned': len(churned), 'retained': len(retained)}
    }


def test_categorical_vs_churn(
    df: pd.DataFrame,
    categorical_col: str,
    target_col: str = 'Churn'
) -> Dict[str, Any]:
    """
    Test association between categorical feature and churn.
    
    Uses Chi-square test with Cramér's V for effect size.
    
    REAL-WORLD NOTE: Check expected frequencies > 5 for validity
    """
    # Create contingency table
    contingency = pd.crosstab(df[categorical_col], df[target_col])
    
    # Perform chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency)
    
    # Check if test is valid
    min_expected = expected.min()
    test_valid = min_expected >= 5
    
    if not test_valid:
        logger.warning(f"Chi-square may be invalid for {categorical_col} (min expected: {min_expected:.1f})")
    
    # Calculate Cramér's V for effect size
    n = contingency.sum().sum()
    min_dim = min(contingency.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim))
    
    # Get category with highest churn rate
    churn_rates = {}
    for category in df[categorical_col].unique():
        mask = df[categorical_col] == category
        rate = (df.loc[mask, target_col] == 'Yes').mean()
        churn_rates[str(category)] = float(rate)
    
    highest_risk = max(churn_rates, key=churn_rates.get)
    
    return {
        'chi2_statistic': float(chi2),
        'p_value': float(p_value),
        'cramers_v': float(cramers_v),
        'significant': p_value < 0.05,
        'test_valid': test_valid,
        'degrees_of_freedom': int(dof),
        'churn_rates_by_category': churn_rates,
        'highest_risk_category': highest_risk
    }


def identify_risk_segments(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identify high-risk customer segments using statistical analysis.
    
    BUSINESS VALUE: This is what executives care about!
    """
    segments = {}
    
    # Segment 1: New customers (tenure < 12) with month-to-month contracts
    mask_high_risk = (df['tenure'] < 12) & (df['Contract'] == 'Month-to-month')
    high_risk_churn = (df.loc[mask_high_risk, 'Churn'] == 'Yes').mean()
    
    segments['new_monthly'] = {
        'description': 'New customers (<1 year) with month-to-month contracts',
        'size': mask_high_risk.sum(),
        'percentage_of_base': float(mask_high_risk.mean() * 100),
        'churn_rate': float(high_risk_churn * 100),
        'risk_level': 'HIGH' if high_risk_churn > 0.4 else 'MEDIUM'
    }
    
    # Segment 2: Electronic check users
    mask_echeck = df['PaymentMethod'] == 'Electronic check'
    echeck_churn = (df.loc[mask_echeck, 'Churn'] == 'Yes').mean()
    
    segments['electronic_check'] = {
        'description': 'Customers paying by electronic check',
        'size': mask_echeck.sum(),
        'percentage_of_base': float(mask_echeck.mean() * 100),
        'churn_rate': float(echeck_churn * 100),
        'risk_level': 'HIGH' if echeck_churn > 0.4 else 'MEDIUM'
    }
    
    # Calculate potential revenue impact
    overall_churn_rate = (df['Churn'] == 'Yes').mean()
    
    for segment_name, segment_data in segments.items():
        # Revenue at risk calculation
        if segment_name == 'new_monthly':
            mask = mask_high_risk
        else:
            mask = mask_echeck
            
        avg_monthly_charges = df.loc[mask, 'MonthlyCharges'].mean()
        segment_data['avg_monthly_charges'] = float(avg_monthly_charges)
        segment_data['monthly_revenue_at_risk'] = float(
            segment_data['size'] * segment_data['churn_rate'] / 100 * avg_monthly_charges
        )
    
    return segments