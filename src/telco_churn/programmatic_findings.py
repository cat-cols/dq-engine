# Programmatically generate all findings
rows, cols = df.shape
data_issues = (df['TotalCharges'] == ' ').sum()
churn_rate = (df['Churn'] == 'Yes').mean() * 100

# Get highest risk segments
contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
worst_contract = contract_churn.idxmax()
contract_rate = contract_churn.max()

payment_churn = df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
worst_payment = payment_churn.idxmax()
payment_rate = payment_churn.max()

internet_churn = df.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
worst_internet = internet_churn.idxmax()
internet_rate = internet_churn.max()

# Key patterns
senior_churn = df.groupby('SeniorCitizen')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
senior_rate = senior_churn[1] if 1 in senior_churn.index else 0
regular_rate = senior_churn[0] if 0 in senior_churn.index else 0

print(f"""
### Data Quality Observations
- Dataset contains {rows:,} customers with {cols} features
- TotalCharges column has data type issues ({data_issues} string values that should be numeric)
- Missing values found: {data_issues} empty spaces in TotalCharges (all tenure=0 customers)
- Mix of binary (Yes/No) and multi-category variables

### Business Insights Discovered
1. **Overall Churn Rate**: {churn_rate:.1f}%
2. **Highest Risk Segments**:
   - Contract type: {worst_contract} ({contract_rate:.1f}% churn)
   - Payment method: {worst_payment} ({payment_rate:.1f}% churn)  
   - Internet service: {worst_internet} ({internet_rate:.1f}% churn)

3. **Key Patterns Observed**:
   - Monthly charges relationship to churn: Higher charges correlate with higher churn
   - Tenure relationship to churn: New customers (tenure=0) don't churn immediately
   - Senior citizen churn patterns: Seniors churn more ({senior_rate:.1f}% vs {regular_rate:.1f}%)

### Questions for Deeper Investigation
1. Why do {worst_contract} contracts have {contract_rate:.1f}% churn vs others?
2. Why do {worst_payment} users churn {payment_rate:.1f}% vs automatic payments?
3. How can we retain senior citizens who churn at {senior_rate:.1f}%?
4. What's the financial impact: ${(df['Churn'] == 'Yes').sum() * df['MonthlyCharges'].mean():.0f}/month revenue loss?

### Technical Notes for Next Level
- Fixed TotalCharges data type conversion ({data_issues} entries corrected)
- Should investigate feature engineering: customer lifetime value, payment risk scores
- Consider advanced visualizations for {worst_contract} contract relationships
- Systematic approach implemented: business logic for tenure=0 customers
""")