"""
Telco Customer Churn - Exploratory Data Analysis
Simple yet comprehensive EDA for understanding customer churn patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Load the Telco Customer Churn dataset"""
    data_path = Path("data/raw/Telco-Customer-Churn.csv")
    df = pd.read_csv(data_path)
    return df

def basic_info(df):
    """Display basic information about the dataset"""
    print("=" * 50)
    print("DATASET OVERVIEW")
    print("=" * 50)
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nData Types:")
    print(df.dtypes)
    print("\nFirst 5 rows:")
    print(df.head())
    
def check_missing_values(df):
    """Check for missing values and data quality issues"""
    print("\n" + "=" * 50)
    print("DATA QUALITY CHECK")
    print("=" * 50)
    
    # Missing values
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct
    }).sort_values('Missing Count', ascending=False)
    
    print("Missing Values:")
    print(missing_df[missing_df['Missing Count'] > 0])
    
    # Check for empty strings or spaces
    print("\nChecking for empty strings...")
    for col in df.select_dtypes(include=['object']).columns:
        empty_count = (df[col] == '').sum() + (df[col] == ' ').sum()
        if empty_count > 0:
            print(f"{col}: {empty_count} empty values")
    
    # Duplicates
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicates}")

def analyze_target_variable(df):
    """Analyze the target variable (Churn)"""
    print("\n" + "=" * 50)
    print("TARGET VARIABLE ANALYSIS")
    print("=" * 50)
    
    churn_counts = df['Churn'].value_counts()
    churn_pct = df['Churn'].value_counts(normalize=True) * 100
    
    print("Churn Distribution:")
    for val, count, pct in zip(churn_counts.index, churn_counts.values, churn_pct.values):
        print(f"{val}: {count} ({pct:.1f}%)")
    
    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Count plot
    sns.countplot(data=df, x='Churn', ax=ax1)
    ax1.set_title('Churn Distribution')
    ax1.set_ylabel('Count')
    
    # Pie chart
    ax2.pie(churn_counts.values, labels=churn_counts.index, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Churn Percentage')
    
    plt.tight_layout()
    plt.show()

def analyze_numerical_features(df):
    """Analyze numerical features"""
    print("\n" + "=" * 50)
    print("NUMERICAL FEATURES ANALYSIS")
    print("=" * 50)
    
    # Convert TotalCharges to numeric (it might be stored as string)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    
    print("Statistical Summary:")
    print(df[numerical_cols].describe())
    
    # Visualizations
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols):
        # Distribution
        sns.histplot(data=df, x=col, hue='Churn', kde=True, ax=axes[i])
        axes[i].set_title(f'{col} Distribution by Churn')
        
        # Box plot
        sns.boxplot(data=df, x='Churn', y=col, ax=axes[i+3])
        axes[i+3].set_title(f'{col} by Churn Status')
    
    plt.tight_layout()
    plt.show()

def analyze_categorical_features(df):
    """Analyze categorical features"""
    print("\n" + "=" * 50)
    print("CATEGORICAL FEATURES ANALYSIS")
    print("=" * 50)
    
    categorical_cols = [col for col in df.columns if df[col].dtype == 'object' and col not in ['customerID', 'Churn']]
    
    # Key categorical features for visualization
    key_features = ['Contract', 'PaymentMethod', 'InternetService', 'gender', 'SeniorCitizen']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for i, col in enumerate(key_features):
        if i < len(axes):
            # Create crosstab
            ct = pd.crosstab(df[col], df['Churn'], normalize='index') * 100
            ct.plot(kind='bar', ax=axes[i], rot=45)
            axes[i].set_title(f'Churn Rate by {col}')
            axes[i].set_ylabel('Churn Rate (%)')
            axes[i].legend(title='Churn')
    
    # Remove empty subplot
    if len(key_features) < len(axes):
        fig.delaxes(axes[-1])
    
    plt.tight_layout()
    plt.show()
    
    # Print churn rates for key categories
    print("\nChurn Rates by Category:")
    for col in key_features:
        print(f"\n{col}:")
        churn_rate = df.groupby(col)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
        for category, rate in churn_rate.items():
            print(f"  {category}: {rate:.1f}%")

def correlation_analysis(df):
    """Analyze correlations between features"""
    print("\n" + "=" * 50)
    print("CORRELATION ANALYSIS")
    print("=" * 50)
    
    # Convert categorical variables to numerical for correlation
    df_encoded = df.copy()
    
    # Binary encoding for Yes/No columns
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
    for col in binary_cols:
        df_encoded[col] = (df_encoded[col] == 'Yes').astype(int)
    
    # Encode SeniorCitizen (already 0/1)
    # Encode other categorical variables
    categorical_to_encode = ['gender', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
                           'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 
                           'StreamingMovies', 'Contract', 'PaymentMethod']
    
    for col in categorical_to_encode:
        if col in df_encoded.columns:
            df_encoded[col] = pd.Categorical(df_encoded[col]).codes
    
    # Convert TotalCharges to numeric
    df_encoded['TotalCharges'] = pd.to_numeric(df_encoded['TotalCharges'], errors='coerce')
    
    # Select numerical columns for correlation
    numerical_cols = df_encoded.select_dtypes(include=[np.number]).columns
    numerical_cols = [col for col in numerical_cols if col != 'customerID']
    
    # Correlation matrix
    corr_matrix = df_encoded[numerical_cols].corr()
    
    # Plot correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.show()
    
    # Show correlations with Churn
    churn_corr = corr_matrix['Churn'].abs().sort_values(ascending=False)
    print("\nFeatures most correlated with Churn:")
    for feature, corr in churn_corr.items():
        if feature != 'Churn':
            print(f"{feature}: {corr:.3f}")

def generate_insights(df):
    """Generate key insights from the analysis"""
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)
    
    # Convert TotalCharges to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    insights = []
    
    # Churn rate
    churn_rate = (df['Churn'] == 'Yes').mean() * 100
    insights.append(f"Overall churn rate: {churn_rate:.1f}%")
    
    # Contract insights
    contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    insights.append(f"Month-to-month contracts have highest churn: {contract_churn['Month-to-month']:.1f}%")
    
    # Tenure insights
    avg_tenure_churned = df[df['Churn'] == 'Yes']['tenure'].mean()
    avg_tenure_retained = df[df['Churn'] == 'No']['tenure'].mean()
    insights.append(f"Average tenure - Churned: {avg_tenure_churned:.1f} months, Retained: {avg_tenure_retained:.1f} months")
    
    # Payment method insights
    payment_churn = df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    highest_churn_payment = payment_churn.idxmax()
    insights.append(f"Highest churn payment method: {highest_churn_payment} ({payment_churn[highest_churn_payment]:.1f}%)")
    
    # Internet service insights
    internet_churn = df.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    insights.append(f"Fiber optic users have higher churn: {internet_churn['Fiber optic']:.1f}%")
    
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")

def main():
    """Main function to run the complete EDA"""
    print("Starting Telco Customer Churn EDA...")
    
    # Load data
    df = load_data()
    
    # Run analysis
    basic_info(df)
    check_missing_values(df)
    analyze_target_variable(df)
    analyze_numerical_features(df)
    analyze_categorical_features(df)
    correlation_analysis(df)
    generate_insights(df)
    
    print("\n" + "=" * 60)
    print("EDA COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    main()

################
# """
# Telco Customer Churn - Exploratory Data Analysis
# Simple yet comprehensive EDA for understanding customer churn patterns
# """

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from pathlib import Path

# # Set style for better visualizations
# plt.style.use('seaborn-v0_8')
# sns.set_palette("husl")

# def load_data():
#     """Load the Telco Customer Churn dataset"""
#     data_path = Path("data/raw/Telco-Customer-Churn.csv")
#     df = pd.read_csv(data_path)
#     return df

# def basic_info(df):
#     """Display basic information about the dataset"""
#     print("=" * 50)
#     print("DATASET OVERVIEW")
#     print("=" * 50)
#     print(f"Shape: {df.shape}")
#     print(f"Columns: {df.columns.tolist()}")
#     print("\nData Types:")
#     print(df.dtypes)
#     print("\nFirst 5 rows:")
#     print(df.head())
    
# def check_missing_values(df):
#     """Check for missing values and data quality issues"""
#     print("\n" + "=" * 50)
#     print("DATA QUALITY CHECK")
#     print("=" * 50)
    
#     # Missing values
#     missing = df.isnull().sum()
#     missing_pct = (missing / len(df)) * 100
#     missing_df = pd.DataFrame({
#         'Missing Count': missing,
#         'Missing %': missing_pct
#     }).sort_values('Missing Count', ascending=False)
    
#     print("Missing Values:")
#     print(missing_df[missing_df['Missing Count'] > 0])
    
#     # Check for empty strings or spaces
#     print("\nChecking for empty strings...")
#     for col in df.select_dtypes(include=['object']).columns:
#         empty_count = (df[col] == '').sum() + (df[col] == ' ').sum()
#         if empty_count > 0:
#             print(f"{col}: {empty_count} empty values")
    
#     # Duplicates
#     duplicates = df.duplicated().sum()
#     print(f"\nDuplicate rows: {duplicates}")

# def analyze_target_variable(df):
#     """Analyze the target variable (Churn)"""
#     print("\n" + "=" * 50)
#     print("TARGET VARIABLE ANALYSIS")
#     print("=" * 50)
    
#     churn_counts = df['Churn'].value_counts()
#     churn_pct = df['Churn'].value_counts(normalize=True) * 100
    
#     print("Churn Distribution:")
#     for val, count, pct in zip(churn_counts.index, churn_counts.values, churn_pct.values):
#         print(f"{val}: {count} ({pct:.1f}%)")
    
#     # Visualization
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
#     # Count plot
#     sns.countplot(data=df, x='Churn', ax=ax1)
#     ax1.set_title('Churn Distribution')
#     ax1.set_ylabel('Count')
    
#     # Pie chart
#     ax2.pie(churn_counts.values, labels=churn_counts.index, autopct='%1.1f%%', startangle=90)
#     ax2.set_title('Churn Percentage')
    
#     plt.tight_layout()
#     plt.show()

# def analyze_numerical_features(df):
#     """Analyze numerical features"""
#     print("\n" + "=" * 50)
#     print("NUMERICAL FEATURES ANALYSIS")
#     print("=" * 50)
    
#     # Convert TotalCharges to numeric (it might be stored as string)
#     df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
#     numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    
#     print("Statistical Summary:")
#     print(df[numerical_cols].describe())
    
#     # Visualizations
#     fig, axes = plt.subplots(2, 3, figsize=(15, 10))
#     axes = axes.ravel()
    
#     for i, col in enumerate(numerical_cols):
#         # Distribution
#         sns.histplot(data=df, x=col, hue='Churn', kde=True, ax=axes[i])
#         axes[i].set_title(f'{col} Distribution by Churn')
        
#         # Box plot
#         sns.boxplot(data=df, x='Churn', y=col, ax=axes[i+3])
#         axes[i+3].set_title(f'{col} by Churn Status')
    
#     plt.tight_layout()
#     plt.show()

# def analyze_categorical_features(df):
#     """Analyze categorical features"""
#     print("\n" + "=" * 50)
#     print("CATEGORICAL FEATURES ANALYSIS")
#     print("=" * 50)
    
#     categorical_cols = [col for col in df.columns if df[col].dtype == 'object' and col not in ['customerID', 'Churn']]
    
#     # Key categorical features for visualization
#     key_features = ['Contract', 'PaymentMethod', 'InternetService', 'gender', 'SeniorCitizen']
    
#     fig, axes = plt.subplots(2, 3, figsize=(18, 12))
#     axes = axes.ravel()
    
#     for i, col in enumerate(key_features):
#         if i < len(axes):
#             # Create crosstab
#             ct = pd.crosstab(df[col], df['Churn'], normalize='index') * 100
#             ct.plot(kind='bar', ax=axes[i], rot=45)
#             axes[i].set_title(f'Churn Rate by {col}')
#             axes[i].set_ylabel('Churn Rate (%)')
#             axes[i].legend(title='Churn')
    
#     # Remove empty subplot
#     if len(key_features) < len(axes):
#         fig.delaxes(axes[-1])
    
#     plt.tight_layout()
#     plt.show()
    
#     # Print churn rates for key categories
#     print("\nChurn Rates by Category:")
#     for col in key_features:
#         print(f"\n{col}:")
#         churn_rate = df.groupby(col)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
#         for category, rate in churn_rate.items():
#             print(f"  {category}: {rate:.1f}%")

# def correlation_analysis(df):
#     """Analyze correlations between features"""
#     print("\n" + "=" * 50)
#     print("CORRELATION ANALYSIS")
#     print("=" * 50)
    
#     # Convert categorical variables to numerical for correlation
#     df_encoded = df.copy()
    
#     # Binary encoding for Yes/No columns
#     binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
#     for col in binary_cols:
#         df_encoded[col] = (df_encoded[col] == 'Yes').astype(int)
    
#     # Encode SeniorCitizen (already 0/1)
#     # Encode other categorical variables
#     categorical_to_encode = ['gender', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
#                            'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 
#                            'StreamingMovies', 'Contract', 'PaymentMethod']
    
#     for col in categorical_to_encode:
#         if col in df_encoded.columns:
#             df_encoded[col] = pd.Categorical(df_encoded[col]).codes
    
#     # Convert TotalCharges to numeric
#     df_encoded['TotalCharges'] = pd.to_numeric(df_encoded['TotalCharges'], errors='coerce')
    
#     # Select numerical columns for correlation
#     numerical_cols = df_encoded.select_dtypes(include=[np.number]).columns
#     numerical_cols = [col for col in numerical_cols if col != 'customerID']
    
#     # Correlation matrix
#     corr_matrix = df_encoded[numerical_cols].corr()
    
#     # Plot correlation heatmap
#     plt.figure(figsize=(12, 10))
#     sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
#                 square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
#     plt.title('Feature Correlation Matrix')
#     plt.tight_layout()
#     plt.show()
    
#     # Show correlations with Churn
#     churn_corr = corr_matrix['Churn'].abs().sort_values(ascending=False)
#     print("\nFeatures most correlated with Churn:")
#     for feature, corr in churn_corr.items():
#         if feature != 'Churn':
#             print(f"{feature}: {corr:.3f}")

# def generate_insights(df):
#     """Generate key insights from the analysis"""
#     print("\n" + "=" * 60)
#     print("KEY INSIGHTS")
#     print("=" * 60)
    
#     # Convert TotalCharges to numeric
#     df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
#     insights = []
    
#     # Churn rate
#     churn_rate = (df['Churn'] == 'Yes').mean() * 100
#     insights.append(f"Overall churn rate: {churn_rate:.1f}%")
    
#     # Contract insights
#     contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
#     insights.append(f"Month-to-month contracts have highest churn: {contract_churn['Month-to-month']:.1f}%")
    
#     # Tenure insights
#     avg_tenure_churned = df[df['Churn'] == 'Yes']['tenure'].mean()
#     avg_tenure_retained = df[df['Churn'] == 'No']['tenure'].mean()
#     insights.append(f"Average tenure - Churned: {avg_tenure_churned:.1f} months, Retained: {avg_tenure_retained:.1f} months")
    
#     # Payment method insights
#     payment_churn = df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
#     highest_churn_payment = payment_churn.idxmax()
#     insights.append(f"Highest churn payment method: {highest_churn_payment} ({payment_churn[highest_churn_payment]:.1f}%)")
    
#     # Internet service insights
#     internet_churn = df.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
#     insights.append(f"Fiber optic users have higher churn: {internet_churn['Fiber optic']:.1f}%")
    
#     for i, insight in enumerate(insights, 1):
#         print(f"{i}. {insight}")

# def main():
#     """Main function to run the complete EDA"""
#     print("Starting Telco Customer Churn EDA...")
    
#     # Load data
#     df = load_data()
    
#     # Run analysis
#     basic_info(df)
#     check_missing_values(df)
#     analyze_target_variable(df)
#     analyze_numerical_features(df)
#     analyze_categorical_features(df)
#     correlation_analysis(df)
#     generate_insights(df)
    
#     print("\n" + "=" * 60)
#     print("EDA COMPLETED!")
#     print("=" * 60)

# if __name__ == "__main__":
#     main()
