# Let's examine the tenure=0 customers more closely
import pandas as pd

# Look at the problematic customers
problem_customers = df[df['TotalCharges'] == ' ']
print("Customers with missing TotalCharges:")
print(problem_customers[['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']].head())

# Check: Do ALL tenure=0 customers have missing TotalCharges?
all_new_customers = df[df['tenure'] == 0]
print(f"\nAll customers with tenure=0: {len(all_new_customers)}")
print(f"Customers with missing TotalCharges: {len(problem_customers)}")
print(f"Are they the same customers? {len(all_new_customers) == len(problem_customers)}")

# Show a few tenure=0 customers to understand the pattern
print("\nAll tenure=0 customers:")
print(all_new_customers[['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']])

# Business logic check: What should TotalCharges be for tenure=0?
print("\n=== BUSINESS LOGIC ANALYSIS ===")
print("Two possible scenarios:")
print("1. Customer signed up but hasn't been billed yet → TotalCharges = 0")
print("2. Customer signed up and was billed for first month → TotalCharges = MonthlyCharges") 
print("3. Customer signed up, was billed, and churned in same month → TotalCharges = MonthlyCharges")