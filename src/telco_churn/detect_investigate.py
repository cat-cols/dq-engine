# Define the function first
def investigate_column(df, col):
    """Standard data detective routine for any column"""
    print(f"=== INVESTIGATING {col} ===")
    print(f"Data type: {df[col].dtype}")
    print(f"Null count: {df[col].isnull().sum()}")
    print(f"Unique values: {df[col].nunique()}")
    print(f"Sample values: {df[col].head(5).tolist()}")

    if df[col].dtype == 'object':
        print(f"All unique values: {df[col].unique()}")

        # Check if it should be numeric
        print("Testing numeric conversion...")
        converted = pd.to_numeric(df[col], errors='coerce')
        conversion_issues = converted.isnull().sum() - df[col].isnull().sum()
        if conversion_issues > 0:
            print(f"🚨 {conversion_issues} values can't convert to numeric!")
            problematic = df[converted.isnull() & df[col].notnull()][col].unique()
            print(f"Problematic values: {problematic}")

# NOW you can use it
print("=== DATA DETECTIVE WORK ===")

# Check all supposedly numeric columns
numeric_expected = ['TotalCharges', 'MonthlyCharges', 'tenure']
for col in numeric_expected:
    if col in df.columns and df[col].dtype == 'object':
        print(f"🚨 INVESTIGATING: {col} should be numeric but is object")
        investigate_column(df, col)

# Define the function first
def investigate_column(df, col):
    """Standard data detective routine for any column"""
    print(f"=== INVESTIGATING {col} ===")
    print(f"Data type: {df[col].dtype}")
    print(f"Null count: {df[col].isnull().sum()}")
    print(f"Unique values: {df[col].nunique()}")
    print(f"Sample values: {df[col].head(5).tolist()}")
    
    if df[col].dtype == 'object':
        print(f"All unique values: {df[col].unique()}")
        
        # Check if it should be numeric
        print("Testing numeric conversion...")
        converted = pd.to_numeric(df[col], errors='coerce')
        conversion_issues = converted.isnull().sum() - df[col].isnull().sum()
        if conversion_issues > 0:
            print(f"🚨 {conversion_issues} values can't convert to numeric!")
            problematic = df[converted.isnull() & df[col].notnull()][col].unique()
            print(f"Problematic values: {problematic}")

# NOW you can use it
print("=== DATA DETECTIVE WORK ===")

# Check all supposedly numeric columns
numeric_expected = ['TotalCharges', 'MonthlyCharges', 'tenure']
for col in numeric_expected:
    if col in df.columns and df[col].dtype == 'object':
        print(f"🚨 INVESTIGATING: {col} should be numeric but is object")
        investigate_column(df, col)

#!/usr/bin/env python3
"""
TotalCharges Data Quality Detective Script
=========================================
This script systematically investigates the TotalCharges column to identify
and display problematic entries that can't be converted to numeric values.
"""

import pandas as pd
import numpy as np

def investigate_totalcharges(csv_file_path):
    """
    Investigate TotalCharges column for data quality issues
    
    Args:
        csv_file_path (str): Path to the telco.csv file
    """
    
    print("🔍 TOTALCHARGES DATA QUALITY INVESTIGATION")
    print("=" * 55)
    
    # Load the data
    try:
        df = pd.read_csv(csv_file_path)
        print(f"✅ Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    print("\n" + "="*55)
    
    # Step 1: Check the data type
    print("STEP 1: DATA TYPE INVESTIGATION")
    print("-" * 30)
    print(f"TotalCharges data type: {df['TotalCharges'].dtype}")
    
    if df['TotalCharges'].dtype == 'object':
        print("🚨 RED FLAG: TotalCharges should be numeric but is stored as text!")
    else:
        print("✅ Data type looks correct")
    
    print("\n" + "="*55)
    
    # Step 2: Show sample values
    print("STEP 2: SAMPLE VALUES INSPECTION")
    print("-" * 32)
    print("First 10 TotalCharges values:")
    for i, val in enumerate(df['TotalCharges'].head(10)):
        print(f"  Row {i}: '{val}' (type: {type(val).__name__})")
    
    print("\n" + "="*55)
    
    # Step 3: Test numeric conversion
    print("STEP 3: NUMERIC CONVERSION TEST")
    print("-" * 31)
    
    # Try conversion with error catching
    df['TotalCharges_numeric'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Count conversion issues
    original_nulls = df['TotalCharges'].isnull().sum()
    converted_nulls = df['TotalCharges_numeric'].isnull().sum()
    conversion_failures = converted_nulls - original_nulls
    
    print(f"Original null values: {original_nulls}")
    print(f"Nulls after conversion: {converted_nulls}")
    print(f"Values that failed conversion: {conversion_failures}")
    
    if conversion_failures > 0:
        print(f"🚨 PROBLEM DETECTED: {conversion_failures} values couldn't be converted!")
    else:
        print("✅ All values converted successfully")
    
    print("\n" + "="*55)
    
    # Step 4: Identify and display problem entries
    if conversion_failures > 0:
        print("STEP 4: PROBLEM ENTRIES ANALYSIS")
        print("-" * 32)
        
        # Find rows where conversion failed
        problem_mask = (df['TotalCharges_numeric'].isnull()) & (df['TotalCharges'].notnull())
        problem_rows = df[problem_mask]
        
        print(f"Found {len(problem_rows)} problematic rows:")
        print("\nPROBLEMATIC VALUES:")
        
        # Show unique problematic values
        problem_values = problem_rows['TotalCharges'].unique()
        for val in problem_values:
            count = (problem_rows['TotalCharges'] == val).sum()
            print(f"  Value: '{val}' | Count: {count} | Length: {len(str(val))} characters")
            
            # Show character analysis for weird values
            if val.strip() != val or len(val.strip()) == 0:
                print(f"    🔍 Special analysis: repr='{repr(val)}'")
        
        print("\nSAMPLE PROBLEM ROWS:")
        # Show a few complete rows for context
        display_cols = ['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges']
        sample_problems = problem_rows[display_cols].head(5)
        print(sample_problems.to_string(index=False))
        
        print("\n" + "="*55)
        
        # Step 5: Business logic check
        print("STEP 5: BUSINESS LOGIC ANALYSIS")
        print("-" * 31)
        
        # Check if these customers have zero tenure (might explain empty TotalCharges)
        zero_tenure_problems = problem_rows[problem_rows['tenure'] == 0]
        print(f"Problem entries with zero tenure: {len(zero_tenure_problems)}")
        
        if len(zero_tenure_problems) > 0:
            print("💡 INSIGHT: Customers with zero tenure might legitimately have no total charges")
            print("Sample zero tenure customers:")
            print(zero_tenure_problems[['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges']].head(3).to_string(index=False))
    
    print("\n" + "="*55)
    
    # Step 6: Summary and recommendations
    print("STEP 6: SUMMARY & RECOMMENDATIONS")
    print("-" * 34)
    
    if conversion_failures > 0:
        print("🔧 DATA CLEANING NEEDED:")
        print("  1. Convert problematic values to NaN or 0")
        print("  2. Investigate business rules for empty values") 
        print("  3. Consider if zero tenure customers should have TotalCharges = 0")
        
        print("\n💻 SUGGESTED CLEANING CODE:")
        print("  # Replace problematic values with NaN")
        print("  df['TotalCharges_clean'] = pd.to_numeric(df['TotalCharges'], errors='coerce')")
        print("  ")
        print("  # Or replace with 0 for zero tenure customers")
        print("  df['TotalCharges_clean'] = df['TotalCharges_clean'].fillna(0)")
    else:
        print("✅ NO CLEANING NEEDED - All values are numeric!")
    
    return df

def main():
    """Main function to run the investigation"""
    
    # File path - adjust this to your actual file location
    csv_file_path = 'data/telco.csv'  # Adjust path as needed
    
    print("TotalCharges Data Quality Detective")
    print("=" * 35)
    print("This script will investigate the TotalCharges column for data quality issues.")
    print(f"Looking for file: {csv_file_path}")
    print()
    
    # Run the investigation
    df = investigate_totalcharges(csv_file_path)
    
    if df is not None:
        print("\n🎯 INVESTIGATION COMPLETE!")
        print("Review the findings above to understand what data cleaning is needed.")

if __name__ == "__main__":
    main()