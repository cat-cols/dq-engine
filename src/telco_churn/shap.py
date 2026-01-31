# SHAP
import shap
import matplotlib.pyplot as plt
import pandas as pd

# Sample: use a smaller subset if dataset is large
X_sample = X_test.sample(1000, random_state=42)

# Compute SHAP interaction values
explainer = shap.TreeExplainer(rf_model)
shap_interaction_values = explainer.shap_interaction_values(X_sample)

# Pick top 3 features by mean absolute SHAP value
mean_abs_shap = pd.DataFrame(shap_interaction_values, columns=X_sample.columns).abs().mean().sort_values(ascending=False)
top_features = mean_abs_shap.head(3).index.tolist()

# Create a readable summary plot for interactions among top 3 features
for i, feature_i in enumerate(top_features):
    for j, feature_j in enumerate(top_features):
        if i <= j:  # only upper triangle including diagonal
            shap.dependence_plot(
                (i, j) if i != j else feature_i,  # pair for interaction or single feature
                shap_interaction_values,
                X_sample,
                interaction_index=j if i != j else None,
                show=False,
                alpha=0.7,
                dot_size=15,
                title=f"Interaction: {feature_i} x {feature_j}" if i != j else f"Main effect: {feature_i}"
            )
            plt.colorbar(label='Feature Value (Blue=Low, Red=High)')
            plt.tight_layout()
            plt.show()


# ============================================
# 4b. SHAP Summary for Churn=Yes (Class 1)
# ============================================

# If model predicts probabilities for 2 classes, shap_values.values.shape[1] > 1
if shap_values.values.shape[1] > 1:
    # Extract SHAP values for Churn=Yes (class 1)
    shap_values_class1 = shap_values[:, 1]
    
    # Summary plot for class 1
    shap.summary_plot(
        shap_values_class1,
        X_test_sample,
        plot_type='dot',       # Dot plot shows distribution
        color=plt.get_cmap('coolwarm'),  # Intuitive color: blue=low, red=high
        alpha=0.7,             # Slight transparency for dense areas
        show=True
    )

# ============================================
# 3. SHAP with new API
# ============================================

explainer = shap.Explainer(rf_model, X_train)
shap_values = explainer(X_test.sample(500, random_state=42))  # sample for speed

# Summary plot
shap.summary_plot(shap_values, X_test.sample(500, random_state=42))

# ============================================
# 2. EXPLORATORY DATA ANALYSIS VISUALIZATIONS
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/b/DATA/PROJECTS/Telco/resources/data/processed/telco_cleaned.csv')

def create_eda_dashboard(df):
    """Create comprehensive EDA dashboard"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Telco Customer Churn - Exploratory Data Analysis', fontsize=16, y=1.02)
    
    # 1. Churn Distribution
    churn_counts = df['Churn'].value_counts()
    colors = ['#2E7D32', '#C62828']
    axes[0,0].pie(churn_counts.values, labels=churn_counts.index, autopct='%1.1f%%',
                  colors=colors, startangle=90)
    axes[0,0].set_title('Overall Churn Rate', fontsize=12, fontweight='bold')
    
    # 2. Churn by Contract Type
    churn_by_contract = df.groupby('Contract')['Churn_Binary'].mean().sort_values()
    bars = axes[0,1].barh(range(len(churn_by_contract)), churn_by_contract.values)
    axes[0,1].set_yticks(range(len(churn_by_contract)))
    axes[0,1].set_yticklabels(churn_by_contract.index)
    axes[0,1].set_xlabel('Churn Rate')
    axes[0,1].set_title('Churn Rate by Contract Type', fontsize=12, fontweight='bold')
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, churn_by_contract.values)):
        axes[0,1].text(val + 0.01, bar.get_y() + bar.get_height()/2, 
                       f'{val:.1%}', va='center')
    
    # 3. Tenure Distribution by Churn
    df[df['Churn']=='Yes']['tenure'].hist(bins=30, alpha=0.7, label='Churned', 
                                          ax=axes[0,2], color='#C62828')
    df[df['Churn']=='No']['tenure'].hist(bins=30, alpha=0.7, label='Retained',
                                         ax=axes[0,2], color='#2E7D32')
    axes[0,2].set_xlabel('Tenure (months)')
    axes[0,2].set_ylabel('Count')
    axes[0,2].set_title('Tenure Distribution by Churn Status', fontsize=12, fontweight='bold')
    axes[0,2].legend()
    
    # 4. Monthly Charges by Churn
    df.boxplot(column='MonthlyCharges', by='Churn', ax=axes[1,0])
    axes[1,0].set_title('Monthly Charges Distribution', fontsize=12, fontweight='bold')
    axes[1,0].set_xlabel('Churn Status')
    axes[1,0].set_ylabel('Monthly Charges ($)')
    plt.sca(axes[1,0])
    plt.xticks([1, 2], ['No', 'Yes'])
    
    # 5. Payment Method Impact
    payment_churn = df.groupby('PaymentMethod')['Churn_Binary'].mean().sort_values()
    bars = axes[1,1].barh(range(len(payment_churn)), payment_churn.values)
    axes[1,1].set_yticks(range(len(payment_churn)))
    axes[1,1].set_yticklabels([method[:20] for method in payment_churn.index])  # Truncate long labels
    axes[1,1].set_xlabel('Churn Rate')
    axes[1,1].set_title('Churn Rate by Payment Method', fontsize=12, fontweight='bold')
    for i, (bar, val) in enumerate(zip(bars, payment_churn.values)):
        axes[1,1].text(val + 0.01, bar.get_y() + bar.get_height()/2,
                       f'{val:.1%}', va='center')
    
    # 6. Internet Service Impact
    internet_churn = df.groupby('InternetService')['Churn_Binary'].mean().sort_values()
    bars = axes[1,2].bar(range(len(internet_churn)), internet_churn.values)
    axes[1,2].set_xticks(range(len(internet_churn)))
    axes[1,2].set_xticklabels(internet_churn.index, rotation=45)
    axes[1,2].set_ylabel('Churn Rate')
    axes[1,2].set_title('Churn Rate by Internet Service', fontsize=12, fontweight='bold')
    for bar, val in zip(bars, internet_churn.values):
        axes[1,2].text(bar.get_x() + bar.get_width()/2, val + 0.01,
                       f'{val:.1%}', ha='center')
    
    plt.tight_layout()
    plt.show()
    
    return fig

# Create the EDA dashboard
eda_fig = create_eda_dashboard(df)

# ============================================

# 3. CORRELATION ANALYSIS


def create_correlation_heatmap(df):
    """Create correlation heatmap for numeric features"""
    
    # Select numeric columns and convert binary columns
    numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Churn_Binary']
    
    # Add binary conversions for categorical variables
    binary_mappings = {
        'gender': {'Male': 1, 'Female': 0},
        'Partner': {'Yes': 1, 'No': 0},
        'Dependents': {'Yes': 1, 'No': 0},
        'PhoneService': {'Yes': 1, 'No': 0},
        'PaperlessBilling': {'Yes': 1, 'No': 0},
    }
    
    df_corr = df[numeric_cols].copy()
    
    for col, mapping in binary_mappings.items():
        df_corr[col] = df[col].map(mapping)
    
    # Calculate correlation matrix
    corr_matrix = df_corr.corr()
    
    # Create heatmap
    plt.figure(figsize=(12, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                square=True, mask=mask, vmin=-1, vmax=1,
                cbar_kws={"shrink": 0.8})
    plt.title('Feature Correlation with Churn', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    return corr_matrix

# Create correlation heatmap
corr_matrix = create_correlation_heatmap(df)

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
