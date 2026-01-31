
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


def generate_executive_summary(df):
    """
    Automatically generate executive summary from telco churn dataset
    """
    
    # Basic dataset metrics
    total_customers = len(df)
    churn_count = (df['Churn'] == 'Yes').sum()
    churn_rate = (churn_count / total_customers) * 100
    
    # Data quality issues
    data_issues = (df['TotalCharges'] == ' ').sum()
    
    # Key risk factors
    contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    highest_risk_contract = contract_churn.idxmax()
    highest_risk_rate = contract_churn.max()
    
    payment_churn = df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    riskiest_payment = payment_churn.idxmax()
    payment_risk_rate = payment_churn.max()
    
    senior_churn = df.groupby('SeniorCitizen')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    senior_risk = senior_churn[1] if 1 in senior_churn.index else 0
    
    # Generate summary
    summary = f"""
# Telco Churn Analysis - Executive Summary

## Key Metrics
- **Total Customers Analyzed:** {total_customers:,}
- **Customers Lost (Churn):** {churn_count:,} ({churn_rate:.1f}%)
- **Revenue at Risk:** ~${churn_count * df['MonthlyCharges'].mean():.0f}/month

## Highest Risk Segments
- **Contract Type:** {highest_risk_contract} customers ({highest_risk_rate:.1f}% churn rate)
- **Payment Method:** {riskiest_payment} users ({payment_risk_rate:.1f}% churn rate)
- **Demographics:** Senior citizens ({senior_risk:.1f}% churn rate)

## Data Quality
- **Issues Found:** {data_issues} billing records corrected
- **Data Completeness:** {((total_customers - data_issues) / total_customers * 100):.1f}%

## Business Impact
- **Monthly Revenue Loss:** ~${(churn_count * df['MonthlyCharges'].mean()):.0f}
- **Annual Revenue at Risk:** ~${(churn_count * df['MonthlyCharges'].mean() * 12):.0f}

## Recommendations
1. **Immediate:** Target {highest_risk_contract} contract customers for retention
2. **Payment:** Investigate why {riskiest_payment} users churn more
3. **Senior Focus:** Develop senior citizen retention program
4. **Data:** Continue monitoring data quality (fixed {data_issues} issues)

---
*Generated automatically on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    return summary

# Generate and save summary
executive_summary = generate_executive_summary(df)
print(executive_summary)

# Save to file
with open('executive_summary.md', 'w') as f:
    f.write(executive_summary)

print("\n📄 Executive summary saved to 'executive_summary.md'")

# Optional: Generate metrics dictionary for further use
def get_summary_metrics(df):
    """Return key metrics as dictionary for dashboards/reports"""
    return {
        'total_customers': len(df),
        'churn_count': (df['Churn'] == 'Yes').sum(),
        'churn_rate': (df['Churn'] == 'Yes').mean() * 100,
        'monthly_revenue_loss': (df['Churn'] == 'Yes').sum() * df['MonthlyCharges'].mean(),
        'highest_risk_contract': df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean()).idxmax(),
        'data_quality_issues': (df['TotalCharges'] == ' ').sum()
    }

# Get metrics for other uses (dashboards, APIs, etc.)
metrics = get_summary_metrics(df)
print("\n📊 Key Metrics Dictionary:")
for key, value in metrics.items():
    print(f"  {key}: {value}")

import pandas as pd
# from datetime import datetime

# def generate_professional_executive_summary(df, analyst_name="Data Analytics Team"):
#     """
#     Generate a professional executive summary for telco churn analysis
    
#     Parameters:
#     -----------
#     df : pandas.DataFrame
#         Telco customer dataset
#     analyst_name : str
#         Name of analyst or team for attribution
    
#     Returns:
#     --------
#     str : Formatted executive summary
#     """
    
#     # Key Metrics Calculation
#     total_customers = len(df)
#     churned_customers = (df['Churn'] == 'Yes').sum()
#     churn_rate = (churned_customers / total_customers) * 100
#     retained_customers = total_customers - churned_customers
    
#     # Risk Analysis
#     contract_analysis = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).round(1)
#     highest_risk_contract = contract_analysis.idxmax()
#     highest_risk_rate = contract_analysis.max()
#     lowest_risk_contract = contract_analysis.idxmin()
#     lowest_risk_rate = contract_analysis.min()
    
#     payment_analysis = df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).round(1)
#     riskiest_payment = payment_analysis.idxmax()
#     riskiest_payment_rate = payment_analysis.max()
    
#     # Financial Impact
#     avg_monthly_charges = df['MonthlyCharges'].mean()
#     monthly_revenue_loss = churned_customers * avg_monthly_charges
#     annual_revenue_impact = monthly_revenue_loss * 12
    
#     # Data Quality Assessment
#     data_quality_issues = (df['TotalCharges'] == ' ').sum()
#     data_completeness = ((total_customers - data_quality_issues) / total_customers) * 100
    
#     # Generate Professional Summary
#     summary = f"""
# TELCO CUSTOMER CHURN ANALYSIS
# EXECUTIVE SUMMARY
# {'=' * 50}

# ANALYSIS OVERVIEW
# Dataset Period: Current customer base analysis
# Analysis Date: {datetime.now().strftime('%B %d, %Y')}
# Analyst: {analyst_name}

# KEY FINDINGS
# Customer Base: {total_customers:,} active customers analyzed
# Churn Impact: {churned_customers:,} customers lost ({churn_rate:.1f}% churn rate)
# Customer Retention: {retained_customers:,} customers retained ({100-churn_rate:.1f}% retention rate)

# FINANCIAL IMPACT
# Monthly Revenue Loss: ${monthly_revenue_loss:,.0f}
# Annualized Revenue Impact: ${annual_revenue_impact:,.0f}
# Average Customer Value: ${avg_monthly_charges:.0f}/month

# RISK ASSESSMENT
# Highest Risk Segment: {highest_risk_contract} contract customers ({highest_risk_rate:.1f}% churn rate)
# Lowest Risk Segment: {lowest_risk_contract} contract customers ({lowest_risk_rate:.1f}% churn rate)
# Payment Risk Factor: {riskiest_payment} users show highest churn ({riskiest_payment_rate:.1f}%)

# DATA QUALITY
# Data Completeness: {data_completeness:.1f}%
# Issues Identified: {data_quality_issues} billing records required correction
# Quality Status: High-quality dataset suitable for predictive modeling

# STRATEGIC RECOMMENDATIONS
# 1. IMMEDIATE ACTIONS (0-30 days)
#    • Target {highest_risk_contract} contract customers for retention campaigns
#    • Investigate {riskiest_payment} payment method friction points
#    • Implement proactive outreach for high-risk customer segments

# 2. TACTICAL INITIATIVES (30-90 days)
#    • Develop contract upgrade incentives to move customers from {highest_risk_contract} to longer terms
#    • Create payment method migration strategies away from {riskiest_payment}
#    • Establish senior citizen retention program (higher risk demographic identified)

# 3. STRATEGIC INVESTMENTS (90+ days)
#    • Build predictive churn model using identified risk factors
#    • Develop customer lifetime value optimization framework
#    • Implement real-time churn risk monitoring system

# BUSINESS IMPACT PROJECTION
# Retention Improvement Target: 5% reduction in churn rate
# Projected Monthly Savings: ${(total_customers * 0.05 * avg_monthly_charges):,.0f}
# Annual Revenue Protection: ${(total_customers * 0.05 * avg_monthly_charges * 12):,.0f}

# {'=' * 50}
# Report prepared by: {analyst_name}
# Confidence Level: High (comprehensive dataset analysis)
# Next Review: Quarterly churn analysis recommended
# """
    
#     return summary

# # Generate Professional Executive Summary
# executive_summary = generate_professional_executive_summary(df, "Level 0 Analysis Team")
# print(executive_summary)

# # Save to file with timestamp
# timestamp = datetime.now().strftime('%Y%m%d_%H%M')
# filename = f'executive_summary_{timestamp}.txt'

# with open(filename, 'w') as f:
#     f.write(executive_summary)

# print(f"\n📄 Professional executive summary saved to: {filename}")

# # Optional: Generate metrics for dashboard/reporting
# summary_metrics = {
#     'analysis_date': datetime.now().strftime('%Y-%m-%d'),
#     'total_customers': len(df),
#     'churn_rate': (df['Churn'] == 'Yes').mean() * 100,
#     'monthly_revenue_loss': (df['Churn'] == 'Yes').sum() * df['MonthlyCharges'].mean(),
#     'highest_risk_segment': df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean()).idxmax(),
#     'data_quality_score': ((len(df) - (df['TotalCharges'] == ' ').sum()) / len(df)) * 100
# }

# print("\n📊 Summary Metrics for Reporting:")
# for key, value in summary_metrics.items():
#     print(f"  {key}: {value}")
