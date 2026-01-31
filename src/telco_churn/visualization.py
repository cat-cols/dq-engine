"""
src/visualization/plots.py

Visualization module for Telco Churn analysis.
Creates publication-quality plots for analysis and reporting.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

# Set default style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)


class TelcoVisualizer:
    """
    Creates visualizations for Telco churn analysis.
    """
    
    def __init__(self, style: str = 'whitegrid'):
        """
        Initialize visualizer with style settings.
        
        Args:
            style (str): Seaborn style
        """
        sns.set_style(style)
        self.colors = {'no_churn': '#2ecc71', 'churn': '#e74c3c'}
    
    def plot_target_distribution(self, df: pd.DataFrame, 
                                target_col: str = 'Churn',
                                save_path: Optional[str] = None) -> None:
        """
        Plot distribution of target variable.
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_col (str): Name of target column
            save_path (str): Path to save figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Count plot
        churn_counts = df[target_col].value_counts()
        churn_counts.plot(kind='bar', ax=axes[0], 
                         color=[self.colors['no_churn'], self.colors['churn']])
        axes[0].set_title('Churn Distribution', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Churn')
        axes[0].set_ylabel('Count')
        axes[0].set_xticklabels(['No', 'Yes'], rotation=0)
        
        # Pie chart
        axes[1].pie(churn_counts, labels=['No Churn', 'Churn'], 
                   autopct='%1.1f%%',
                   colors=[self.colors['no_churn'], self.colors['churn']])
        axes[1].set_title('Churn Percentage', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Figure saved to {save_path}")
        
        plt.show()
    
    def plot_categorical_churn(self, df: pd.DataFrame, 
                              categorical_cols: List[str],
                              target_col: str = 'Churn',
                              save_path: Optional[str] = None) -> None:
        """
        Plot churn rates for categorical features.
        
        Args:
            df (pd.DataFrame): Input dataframe
            categorical_cols (List[str]): List of categorical columns
            target_col (str): Target column name
            save_path (str): Path to save figure
        """
        n_cols = len(categorical_cols)
        n_rows = (n_cols + 2) // 3
        
        fig, axes = plt.subplots(n_rows, 3, figsize=(18, n_rows * 4))
        axes = axes.flatten() if n_cols > 1 else [axes]
        
        for idx, col in enumerate(categorical_cols):
            if col not in df.columns:
                continue
            
            feature_churn = df.groupby([col, target_col]).size().unstack()
            feature_churn_pct = feature_churn.div(
                feature_churn.sum(axis=1), axis=0
            ) * 100
            
            feature_churn_pct.plot(
                kind='bar', ax=axes[idx],
                color=[self.colors['no_churn'], self.colors['churn']]
            )
            axes[idx].set_title(f'Churn Rate by {col}', 
                               fontsize=11, fontweight='bold')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Percentage')
            axes[idx].legend(['No Churn', 'Churn'], fontsize=8)
            axes[idx].tick_params(axis='x', rotation=30, labelsize=8)
        
        # Hide extra subplots
        for idx in range(n_cols, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Figure saved to {save_path}")
        
        plt.show()
    
    def plot_numerical_distributions(self, df: pd.DataFrame,
                                    numerical_cols: List[str],
                                    target_col: str = 'Churn',
                                    save_path: Optional[str] = None) -> None:
        """
        Plot distributions of numerical features by churn status.
        
        Args:
            df (pd.DataFrame): Input dataframe
            numerical_cols (List[str]): List of numerical columns
            target_col (str): Target column name
            save_path (str): Path to save figure
        """
        n_cols = len(numerical_cols)
        fig, axes = plt.subplots(1, n_cols, figsize=(6*n_cols, 5))
        
        if n_cols == 1:
            axes = [axes]
        
        for idx, col in enumerate(numerical_cols):
            if col not in df.columns:
                continue
            
            axes[idx].hist(
                [df[df[target_col]==0][col], df[df[target_col]==1][col]],
                bins=20, label=['No Churn', 'Churn'],
                color=[self.colors['no_churn'], self.colors['churn']]
            )
            axes[idx].set_title(f'{col} Distribution by Churn',
                               fontsize=12, fontweight='bold')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')
            axes[idx].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Figure saved to {save_path}")
        
        plt.show()
    
    def plot_correlation_matrix(self, df: pd.DataFrame,
                               columns: Optional[List[str]] = None,
                               save_path: Optional[str] = None) -> None:
        """
        Plot correlation heatmap.
        
        Args:
            df (pd.DataFrame): Input dataframe
            columns (List[str]): Columns to include
            save_path (str): Path to save figure
        """
        if columns:
            correlation_matrix = df[columns].corr()
        else:
            correlation_matrix = df.select_dtypes(include=[np.number]).corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
                   center=0, fmt='.2f', square=True, linewidths=1)
        plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Figure saved to {save_path}")
        
        plt.show()
    
    def plot_model_comparison(self, results_dict: Dict,
                             save_path: Optional[str] = None) -> None:
        """
        Plot comparison of multiple models.
        
        Args:
            results_dict (Dict): Dictionary of model results
            save_path (str): Path to save figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Metrics comparison
        metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        model_names = list(results_dict.keys())
        
        metric_data = {
            metric: [results_dict[name][metric] for name in model_names]
            for metric in metrics
        }
        
        x = np.arange(len(model_names))
        width = 0.15
        
        for i, metric in enumerate(metrics):
            axes[0].bar(x + i*width, metric_data[metric], width, 
                       label=metric.upper())
        
        axes[0].set_xlabel('Models', fontweight='bold')
        axes[0].set_ylabel('Score', fontweight='bold')
        axes[0].set_title('Model Performance Comparison',
                         fontsize=14, fontweight='bold')
        axes[0].set_xticks(x + width * 2)
        axes[0].set_xticklabels(model_names, rotation=15, ha='right')
        axes[0].legend()
        axes[0].set_ylim([0.5, 1.0])
        axes[0].grid(axis='y', alpha=0.3)
        
        # ROC Curves (if available)
        for name, res in results_dict.items():
            if 'roc_curve' in res:
                roc_data = res['roc_curve']
                axes[1].plot(roc_data['fpr'], roc_data['tpr'],
                           label=f"{name} (AUC={res['roc_auc']:.3f})",
                           linewidth=2)
        
        axes[1].plot([0, 1], [0, 1], 'k--', label='Random')
        axes[1].set_xlabel('False Positive Rate', fontweight='bold')
        axes[1].set_ylabel('True Positive Rate', fontweight='bold')
        axes[1].set_title('ROC Curves', fontsize=14, fontweight='bold')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Figure saved to {save_path}")
        
        plt.show()
    
    def plot_confusion_matrices(self, results_dict: Dict,
                               save_path: Optional[str] = None) -> None:
        """
        Plot confusion matrices for multiple models.
        
        Args:
            results_dict (Dict): Dictionary of model results
            save_path (str): Path to save figure
        """
        n_models = len(results_dict)
        fig, axes = plt.subplots(1, n_models, figsize=(6*n_models, 5))
        
        if n_models == 1:
            axes = [axes]
        
        for idx, (name, res) in enumerate(results_dict.items()):
            cm = res.get('confusion_matrix')
            if cm is None:
                continue
            
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=['No Churn', 'Churn'],
                       yticklabels=['No Churn', 'Churn'])
            axes[idx].set_title(f'{name}\nConfusion Matrix',
                               fontsize=12, fontweight='bold')
            axes[idx].set_ylabel('Actual')
            axes[idx].set_xlabel('Predicted')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Figure saved to {save_path}")
        
        plt.show()
    
    def plot_feature_importance(self, importance_df: pd.DataFrame,
                               top_n: int = 15,
                               save_path: Optional[str] = None) -> None:
        """
        Plot feature importance.
        
        Args:
            importance_df (pd.DataFrame): Feature importance dataframe
            top_n (int): Number of top features to plot
            save_path (str): Path to save figure
        """
        top_features = importance_df.head(top_n)
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Importance', fontweight='bold')
        plt.title(f'Top {top_n} Feature Importances',
                 fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Figure saved to {save_path}")
        
        plt.show()


if __name__ == "__main__":
    # Example usage
    from src.data.loader import load_telco_data
    
    df = load_telco_data("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    
    visualizer = TelcoVisualizer()
    visualizer.plot_target_distribution(df)
    
    categorical_cols = ['Contract', 'PaymentMethod', 'InternetService']
    visualizer.plot_categorical_churn(df, categorical_cols)
    
    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    visualizer.plot_numerical_distributions(df, numerical_cols)



#####

# ============================================
# 2. EXPLORATORY DATA ANALYSIS VISUALIZATIONS
# ============================================

# def create_eda_dashboard(df):
#     """Create comprehensive EDA dashboard"""
    
#     fig, axes = plt.subplots(2, 3, figsize=(18, 12))
#     fig.suptitle('Telco Customer Churn - Exploratory Data Analysis', fontsize=16, y=1.02)
    
#     # 1. Churn Distribution
#     churn_counts = df['Churn'].value_counts()
#     colors = ['#2E7D32', '#C62828']
#     axes[0,0].pie(churn_counts.values, labels=churn_counts.index, autopct='%1.1f%%',
#                   colors=colors, startangle=90)
#     axes[0,0].set_title('Overall Churn Rate', fontsize=12, fontweight='bold')
    
#     # 2. Churn by Contract Type
#     churn_by_contract = df.groupby('Contract')['Churn_Binary'].mean().sort_values()
#     bars = axes[0,1].barh(range(len(churn_by_contract)), churn_by_contract.values)
#     axes[0,1].set_yticks(range(len(churn_by_contract)))
#     axes[0,1].set_yticklabels(churn_by_contract.index)
#     axes[0,1].set_xlabel('Churn Rate')
#     axes[0,1].set_title('Churn Rate by Contract Type', fontsize=12, fontweight='bold')
#     # Add value labels on bars
#     for i, (bar, val) in enumerate(zip(bars, churn_by_contract.values)):
#         axes[0,1].text(val + 0.01, bar.get_y() + bar.get_height()/2, 
#                        f'{val:.1%}', va='center')
    
#     # 3. Tenure Distribution by Churn
#     df[df['Churn']=='Yes']['tenure'].hist(bins=30, alpha=0.7, label='Churned', 
#                                           ax=axes[0,2], color='#C62828')
#     df[df['Churn']=='No']['tenure'].hist(bins=30, alpha=0.7, label='Retained',
#                                          ax=axes[0,2], color='#2E7D32')
#     axes[0,2].set_xlabel('Tenure (months)')
#     axes[0,2].set_ylabel('Count')
#     axes[0,2].set_title('Tenure Distribution by Churn Status', fontsize=12, fontweight='bold')
#     axes[0,2].legend()
    
#     # 4. Monthly Charges by Churn
#     df.boxplot(column='MonthlyCharges', by='Churn', ax=axes[1,0])
#     axes[1,0].set_title('Monthly Charges Distribution', fontsize=12, fontweight='bold')
#     axes[1,0].set_xlabel('Churn Status')
#     axes[1,0].set_ylabel('Monthly Charges ($)')
#     plt.sca(axes[1,0])
#     plt.xticks([1, 2], ['No', 'Yes'])
    
#     # 5. Payment Method Impact
#     payment_churn = df.groupby('PaymentMethod')['Churn_Binary'].mean().sort_values()
#     bars = axes[1,1].barh(range(len(payment_churn)), payment_churn.values)
#     axes[1,1].set_yticks(range(len(payment_churn)))
#     axes[1,1].set_yticklabels([method[:20] for method in payment_churn.index])  # Truncate long labels
#     axes[1,1].set_xlabel('Churn Rate')
#     axes[1,1].set_title('Churn Rate by Payment Method', fontsize=12, fontweight='bold')
#     for i, (bar, val) in enumerate(zip(bars, payment_churn.values)):
#         axes[1,1].text(val + 0.01, bar.get_y() + bar.get_height()/2,
#                        f'{val:.1%}', va='center')
    
#     # 6. Internet Service Impact
#     internet_churn = df.groupby('InternetService')['Churn_Binary'].mean().sort_values()
#     bars = axes[1,2].bar(range(len(internet_churn)), internet_churn.values)
#     axes[1,2].set_xticks(range(len(internet_churn)))
#     axes[1,2].set_xticklabels(internet_churn.index, rotation=45)
#     axes[1,2].set_ylabel('Churn Rate')
#     axes[1,2].set_title('Churn Rate by Internet Service', fontsize=12, fontweight='bold')
#     for bar, val in zip(bars, internet_churn.values):
#         axes[1,2].text(bar.get_x() + bar.get_width()/2, val + 0.01,
#                        f'{val:.1%}', ha='center')
    
#     plt.tight_layout()
#     plt.show()
    
#     return fig

# # Create the EDA dashboard
# eda_fig = create_eda_dashboard(df)

# ============================================
# 3. CORRELATION ANALYSIS
# ============================================

# def create_correlation_heatmap(df):
#     """Create correlation heatmap for numeric features"""
    
#     # Select numeric columns and convert binary columns
#     numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Churn_Binary']
    
#     # Add binary conversions for categorical variables
#     binary_mappings = {
#         'gender': {'Male': 1, 'Female': 0},
#         'Partner': {'Yes': 1, 'No': 0},
#         'Dependents': {'Yes': 1, 'No': 0},
#         'PhoneService': {'Yes': 1, 'No': 0},
#         'PaperlessBilling': {'Yes': 1, 'No': 0},
#     }
    
#     df_corr = df[numeric_cols].copy()
    
#     for col, mapping in binary_mappings.items():
#         df_corr[col] = df[col].map(mapping)
    
#     # Calculate correlation matrix
#     corr_matrix = df_corr.corr()
    
#     # Create heatmap
#     plt.figure(figsize=(12, 8))
#     mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
#     sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
#                 square=True, mask=mask, vmin=-1, vmax=1,
#                 cbar_kws={"shrink": 0.8})
#     plt.title('Feature Correlation with Churn', fontsize=14, fontweight='bold')
#     plt.tight_layout()
#     plt.show()
    
#     return corr_matrix

# ============================================
# 4. ADVANCED SEGMENTATION ANALYSIS
# ============================================

def create_cohort_analysis(df):
    """Create cohort analysis heatmap"""
    
    # Create pivot table for cohort analysis
    cohort_data = pd.crosstab(df['TenureGroup'], df['Contract'], 
                              df['Churn_Binary'], aggfunc='mean')
    
    # Create heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(cohort_data, annot=True, fmt='.1%', cmap='YlOrRd',
                cbar_kws={'label': 'Churn Rate'})
    plt.title('Churn Rate by Tenure and Contract Type', fontsize=14, fontweight='bold')
    plt.xlabel('Contract Type')
    plt.ylabel('Tenure Group (months)')
    plt.tight_layout()
    plt.show()
    
    return cohort_data

# Create cohort analysis
cohort_data = create_cohort_analysis(df)

# ============================================
# 5. INTERACTIVE PLOTLY VISUALIZATIONS
# ============================================

def create_interactive_dashboard(df):
    """Create interactive Plotly dashboard"""
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Churn Rate by Service Combinations',
                       'Customer Value Segmentation',
                       'Tenure vs Monthly Charges',
                       'Churn Probability by Multiple Factors'),
        specs=[[{'type': 'bar'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'bar'}]]
    )
    
    # 1. Service combination analysis
    services = ['PhoneService', 'InternetService', 'OnlineSecurity', 
                'TechSupport', 'StreamingTV', 'StreamingMovies']
    df['ServiceCount'] = df[services].apply(lambda x: sum(x == 'Yes'), axis=1)
    service_churn = df.groupby('ServiceCount')['Churn_Binary'].mean()
    
    fig.add_trace(
        go.Bar(x=service_churn.index, y=service_churn.values,
               text=[f'{v:.1%}' for v in service_churn.values],
               textposition='outside',
               marker_color='lightblue'),
        row=1, col=1
    )
    
    # 2. Customer Value Segmentation
    fig.add_trace(
        go.Scatter(x=df['MonthlyCharges'], y=df['TotalCharges'],
                  mode='markers',
                  marker=dict(
                      color=df['Churn_Binary'],
                      colorscale='RdYlGn_r',
                      showscale=True,
                      size=5,
                      colorbar=dict(title="Churn")
                  ),
                  text=df['tenure'],
                  hovertemplate='Monthly: $%{x}<br>Total: $%{y}<br>Tenure: %{text} months'),
        row=1, col=2
    )
    
    # 3. Tenure vs Monthly Charges with churn overlay
    fig.add_trace(
        go.Scatter(x=df['tenure'], y=df['MonthlyCharges'],
                  mode='markers',
                  marker=dict(
                      color=df['Churn_Binary'],
                      colorscale=['green', 'red'],
                      size=3,
                      opacity=0.6
                  )),
        row=2, col=1
    )
    
    # 4. Multi-factor churn analysis
    multi_factor = df.groupby(['Contract', 'PaymentMethod'])['Churn_Binary'].mean().reset_index()
    multi_factor['Combined'] = multi_factor['Contract'] + ' - ' + multi_factor['PaymentMethod'].str[:15]
    multi_factor = multi_factor.sort_values('Churn_Binary')
    
    fig.add_trace(
        go.Bar(x=multi_factor['Churn_Binary'], y=multi_factor['Combined'],
               orientation='h',
               text=[f'{v:.1%}' for v in multi_factor['Churn_Binary']],
               textposition='outside'),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(height=800, showlegend=False,
                     title_text="Interactive Churn Analysis Dashboard",
                     title_font_size=16)
    
    # Update axes
    fig.update_xaxes(title_text="Number of Services", row=1, col=1)
    fig.update_yaxes(title_text="Churn Rate", row=1, col=1)
    fig.update_xaxes(title_text="Monthly Charges ($)", row=1, col=2)
    fig.update_yaxes(title_text="Total Charges ($)", row=1, col=2)
    fig.update_xaxes(title_text="Tenure (months)", row=2, col=1)
    fig.update_yaxes(title_text="Monthly Charges ($)", row=2, col=1)
    fig.update_xaxes(title_text="Churn Rate", row=2, col=2)
    
    fig.show()
    
    return fig

# Create interactive dashboard
interactive_fig = create_interactive_dashboard(df)

# ============================================
# 6. FEATURE IMPORTANCE FROM ML MODEL
# ============================================

def calculate_feature_importance(df):
    """Calculate and visualize feature importance using Random Forest"""
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    
    # Prepare data for modeling
    df_model = df.copy()
    
    # Select relevant features
    feature_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Contract',
                   'PaymentMethod', 'InternetService', 'OnlineSecurity',
                   'TechSupport', 'DeviceProtection', 'StreamingTV',
                   'StreamingMovies', 'PaperlessBilling', 'Partner',
                   'Dependents', 'PhoneService', 'MultipleLines']
    
    # Encode categorical variables
    le = LabelEncoder()
    for col in feature_cols:
        if df_model[col].dtype == 'object':
            df_model[col + '_Encoded'] = le.fit_transform(df_model[col].fillna('None'))
            feature_cols[feature_cols.index(col)] = col + '_Encoded'
    
    # Prepare X and y
    X = df_model[feature_cols]
    y = df_model['Churn_Binary']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    rf_model.fit(X_train, y_train)
    
    # Get feature importance
    feature_importance = pd.DataFrame({
        'feature': [col.replace('_Encoded', '') for col in X.columns],
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=True).tail(15)  # Top 15 features
    
    # Visualize
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(feature_importance)), feature_importance['importance'])
    plt.yticks(range(len(feature_importance)), feature_importance['feature'])
    plt.xlabel('Feature Importance')
    plt.title('Top 15 Features Driving Customer Churn', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Add value labels
    for i, val in enumerate(feature_importance['importance']):
        plt.text(val + 0.001, i, f'{val:.3f}', va='center')
    
    plt.show()
    
    return rf_model, feature_importance

# Calculate feature importance
rf_model, feature_importance = calculate_feature_importance(df)

# ============================================
# 7. CHURN RISK SCORING
# ============================================

def create_risk_segments(df, model=None):
    """Create customer risk segments based on churn probability"""
    
    # If model is provided, use it to predict probabilities
    # Otherwise, use simple rule-based scoring
    
    if model:
        # This would use the actual model predictions
        # For demonstration, we'll use rule-based scoring
        pass
    
    # Simple risk scoring based on key factors
    risk_score = pd.Series(0, index=df.index)
    
    # High-risk factors
    risk_score += (df['Contract'] == 'Month-to-month') * 30
    risk_score += (df['tenure'] < 12) * 25
    risk_score += (df['PaymentMethod'] == 'Electronic check') * 20
    risk_score += (df['InternetService'] == 'Fiber optic') * 10
    risk_score += (df['OnlineSecurity'] == 'No') * 15
    risk_score += (df['TechSupport'] == 'No') * 15
    risk_score += (df['MonthlyCharges'] > 70) * 10
    
    # Protective factors
    risk_score -= (df['Contract'].isin(['One year', 'Two year'])) * 20
    risk_score -= (df['tenure'] > 24) * 15
    risk_score -= (df['Dependents'] == 'Yes') * 10
    risk_score -= (df['Partner'] == 'Yes') * 5
    
    # Normalize to 0-100
    risk_score = (risk_score - risk_score.min()) / (risk_score.max() - risk_score.min()) * 100
    
    # Create risk categories
    df['RiskScore'] = risk_score
    df['RiskCategory'] = pd.cut(risk_score, bins=[0, 25, 50, 75, 100],
                                labels=['Low', 'Medium', 'High', 'Critical'])
    
    # Visualize risk distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Risk score distribution
    axes[0].hist(risk_score, bins=30, edgecolor='black', alpha=0.7)
    axes[0].axvline(risk_score.mean(), color='red', linestyle='--', label=f'Mean: {risk_score.mean():.1f}')
    axes[0].set_xlabel('Risk Score')
    axes[0].set_ylabel('Number of Customers')
    axes[0].set_title('Customer Risk Score Distribution', fontsize=12, fontweight='bold')
    axes[0].legend()
    
    # Risk category vs actual churn
    risk_churn = df.groupby('RiskCategory')['Churn_Binary'].agg(['mean', 'count'])
    x = range(len(risk_churn))
    bars = axes[1].bar(x, risk_churn['mean'])
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(risk_churn.index)
    axes[1].set_ylabel('Actual Churn Rate')
    axes[1].set_xlabel('Risk Category')
    axes[1].set_title('Validation: Risk Category vs Actual Churn', fontsize=12, fontweight='bold')
    
    # Add value and count labels
    for i, (bar, rate, count) in enumerate(zip(bars, risk_churn['mean'], risk_churn['count'])):
        axes[1].text(bar.get_x() + bar.get_width()/2, rate + 0.01,
                    f'{rate:.1%}\n(n={count})', ha='center')
    
    plt.tight_layout()
    plt.show()
    
    return df

# Create risk segments
df = create_risk_segments(df)

# ============================================
# 8. ACTIONABLE INSIGHTS SUMMARY
# ============================================

def generate_insights_summary(df):
    """Generate key insights and recommendations"""
    
    insights = []
    
    # Calculate key metrics
    overall_churn = df['Churn_Binary'].mean()
    
    # Contract insights
    contract_churn = df.groupby('Contract')['Churn_Binary'].mean()
    month_to_month_churn = contract_churn['Month-to-month']
    yearly_churn = contract_churn[contract_churn.index != 'Month-to-month'].mean()
    
    insights.append(f"📊 Overall churn rate: {overall_churn:.1%}")
    insights.append(f"📈 Month-to-month contracts have {month_to_month_churn/yearly_churn:.1f}x higher churn than yearly contracts")
    
    # Tenure insights
    new_customer_churn = df[df['tenure'] <= 6]['Churn_Binary'].mean()
    established_churn = df[df['tenure'] > 24]['Churn_Binary'].mean()
    
    insights.append(f"🆕 New customers (<6 months) churn rate: {new_customer_churn:.1%}")
    insights.append(f"💎 Established customers (>24 months) churn rate: {established_churn:.1%}")
    
    # Service insights
    with_security = df[df['OnlineSecurity'] == 'Yes']['Churn_Binary'].mean()
    without_security = df[df['OnlineSecurity'] == 'No']['Churn_Binary'].mean()
    
    insights.append(f"🔒 Online security reduces churn by {(without_security - with_security)/without_security:.0%}")
    
    # Payment method insights
    electronic_check_churn = df[df['PaymentMethod'] == 'Electronic check']['Churn_Binary'].mean()
    other_payment_churn = df[df['PaymentMethod'] != 'Electronic check']['Churn_Binary'].mean()
    
    insights.append(f"💳 Electronic check users have {electronic_check_churn/other_payment_churn:.1f}x higher churn")
    
    print("\n" + "="*60)
    print("KEY INSIGHTS FROM TELCO CHURN ANALYSIS")
    print("="*60)
    for insight in insights:
        print(f"\n{insight}")
    
    print("\n" + "="*60)
    print("RECOMMENDED ACTIONS")
    print("="*60)
    recommendations = [
        "1. Target month-to-month customers after 3 months with annual contract offers",
        "2. Implement intensive onboarding program for first 6 months",
        "3. Bundle online security and tech support as promotional offers",
        "4. Incentivize switching from electronic check to auto-pay credit card",
        "5. Create loyalty rewards program for 12+ month customers",
        "6. Proactive outreach to high-risk segments with personalized retention offers"
    ]
    
    for rec in recommendations:
        print(f"\n{rec}")
    
    return insights, recommendations

# Generate insights summary
insights, recommendations = generate_insights_summary(df)

print("\n✅ Analysis complete! All visualizations have been generated.")
print("📊 Dataset shape:", df.shape)
print("🎯 Target variable distribution:")
print(df['Churn'].value_counts())

# Payment method insights
electronic_check_churn = df[df['PaymentMethod'] == 'Electronic check']['Churn_Binary'].mean()
other_payment_churn = df[df['PaymentMethod'] != 'Electronic check']['Churn_Binary'].mean()

insights.append(f"💳 Electronic check users have {electronic_check_churn/other_payment_churn:.1f}x higher churn")

print("\n" + "="*60)
